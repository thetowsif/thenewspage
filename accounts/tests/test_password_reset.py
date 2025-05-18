
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.core import mail
from django.test import TestCase
from django.urls import reverse


class PasswordResetTestCase(TestCase):
    """
    A unit test case for the default password reset behavior in Django,
    that is included in the 'auth' package.
    """
    PASSWORD_RESET_URL = reverse('password_reset')
    PASSWORD_RESET_DONE_URL = reverse('password_reset_done')

    def setUp(self):
        """
        This method creates objects in a test database that are available to
        all unit tests. It is called before every unit test run.
        """
        # Custom user model used by this project
        user_model = get_user_model()

        # Test user
        self.user = user_model.objects.create_user(
            username='test_user',
            password='test_pass',
            email='test@example.net',
            age=18
        )

    def test_password_reset_form_render_user_not_authenticated(self):
        """
        Checks that a non-authenticated user can access the password reset form.
        """
        # HTTP Response
        response = self.client.get(path=self.PASSWORD_RESET_URL)

        # Checks that an HTTP 200 (OK) status code is returned.
        self.assertEqual(
            first=response.status_code,
            second=200
        )

        # Checks that the view sends a form of the correct class in the context.
        self.assertIsInstance(
            obj=response.context['form'],
            cls=PasswordResetForm
        )

        # Checks that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='registration/password_reset_form.html'
        )

    def test_password_reset_form_render_user_authenticated(self):
        """
        Checks that an authenticated user can access the password reset form.
        """
        self.client.login(
            username='test_user',
            password='test_pass'
        )

        # Execute the same unit tests for a not-authenticated user
        self.test_password_reset_form_render_user_not_authenticated()

    def test_password_reset_form_submit_user_not_authenticated(self):
        """
        Checks that a non-authenticated user can send their email address in the
        password reset form.
        """

        form_data = {
            'email': 'test@example.net'
        }

        # HTTP Response
        response = self.client.post(
            path=self.PASSWORD_RESET_URL,
            data=form_data,
            follow=True
        )

        # Checks that there is a redirect to the 'password_change_done' page
        self.assertRedirects(
            response=response,
            expected_url=self.PASSWORD_RESET_DONE_URL,
            status_code=302,
            target_status_code=200
        )

        # Checks that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='registration/password_reset_done.html'
        )

        # Checks that one reset password email was sent
        self.assertEqual(
            first=len(mail.outbox),
            second=1
        )

        # Checks that the reset password email was sent to the user
        self.assertEqual(
            first=mail.outbox[0].to,
            second=['test@example.net']
        )

    def test_password_reset_form_submit_user_authenticated(self):
        """
        Checks that an authenticated user can send their email address in the
        password reset form.
        """
        self.client.login(
            username='test_user',
            password='test_pass'
        )

        # Execute the same unit tests for a not-authenticated user
        self.test_password_reset_form_submit_user_not_authenticated()

    def test_password_reset_confirm_form_render(self):
        """
        Verify that a user that receives a password reset email can view
        the password reset form.
        """
        # The password reset link UID and token are obtained from the email
        reset_form_data = {
            'email': 'test@example.net'
        }

        response = self.client.post(
            path=self.PASSWORD_RESET_URL,
            data=reset_form_data
        )

        uid = response.context[0]['uid']
        token = response.context['token']

        # HTTP Response: GET Request to password reset confirm URL
        reset_confirm_url = reverse(
            viewname='password_reset_confirm',
            kwargs={
                'uidb64': uid,
                'token': token
            }
        )

        response = self.client.get(
            path=reset_confirm_url,
            follow=True
        )

        # Checks that an HTTP 200 (OK) status code is returned.
        self.assertEqual(
            first=response.status_code,
            second=200
        )

        # Checks that the view sends a form of the correct class in the context.
        self.assertIsInstance(
            obj=response.context['form'],
            cls=SetPasswordForm
        )

        # Verify that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='registration/password_reset_confirm.html'
        )

    def test_password_reset_confirm_form_submit(self):
        """
        Checks that a user can send their new password using the 'password reset
        confirm' form.
        """
        # The password reset link UID and token are obtained from the email
        reset_form_data = {
            'email': 'test@example.net'
        }

        response = self.client.post(
            path=self.PASSWORD_RESET_URL,
            data=reset_form_data
        )

        uid = response.context[0]['uid']
        token = response.context['token']

        # HTTP Response: GET Request to password reset confirm URL
        # (for token validation)
        reset_confirm_url = reverse(
            viewname='password_reset_confirm',
            kwargs={
                'uidb64': uid,
                'token': token
            }
        )

        self.client.get(
            path=reset_confirm_url,
            follow=True
        )

        # HTTP Response for a POST Request to 'password reset confirms' URL
        # (to establish a new password).
        reset_confirm_url = reverse(
            viewname='password_reset_confirm',
            kwargs={
                'uidb64': uid,
                'token': 'set-password'
            }
        )

        response = self.client.post(
            path=reset_confirm_url,
            data={
                'new_password1': 'new_pass123',
                'new_password2': 'new_pass123'
            },
            follow=True
        )

        # Checks that there is a redirect to the 'password_reset_complete' page
        self.assertRedirects(
            response=response,
            expected_url=reverse('password_reset_complete'),
            status_code=302,
            target_status_code=200
        )

        # Verify that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='registration/password_reset_complete.html'
        )

        # Verify that the user password has changed
        user_model = get_user_model()
        user = user_model.objects.get(username='test_user')

        self.assertFalse(user.check_password('test_pass'))

    def test_invalid_password_reset_confirm_form_submit(self):
        """
        Checks that a user cannot send their new password
        using the 'password reset confirm' form with invalid data.
        """
        # The password reset link UID and token are obtained from the email
        reset_form_data = {
            'email': 'test@example.net'
        }

        response = self.client.post(
            path=self.PASSWORD_RESET_URL,
            data=reset_form_data
        )

        uid = response.context[0]['uid']
        token = response.context['token']

        # HTTP Response: GET Request to password reset confirm URL
        # (for token validation)
        reset_confirm_url = reverse(
            viewname='password_reset_confirm',
            kwargs={
                'uidb64': uid,
                'token': token
            }
        )

        self.client.get(
            path=reset_confirm_url,
            follow=True
        )

        # HTTP Response for a POST Request to 'password reset confirms' URL
        # (to establish a new password).
        reset_confirm_url = reverse(
            viewname='password_reset_confirm',
            kwargs={
                'uidb64': uid,
                'token': 'set-password'
            }
        )

        response = self.client.post(
            path=reset_confirm_url,
            data={
                'new_password1': 'new_pass123',
                'new_password2': 'another_pass'
            },
            follow=True
        )

        # Checks that an HTTP 200 (OK) status code is returned.
        self.assertEqual(
            first=response.status_code,
            second=200
        )

        # Checks that the view sends a form of the correct class in the context.
        self.assertIsInstance(
            obj=response.context['form'],
            cls=SetPasswordForm
        )

        # Checks if the form contains errors
        self.assertTrue(
            expr=response.context['form'].errors
        )

        # Checks that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='registration/password_reset_confirm.html'
        )

        # Checks that the user password is the same
        user_model = get_user_model()
        user = user_model.objects.get(username='test_user')
        self.assertTrue(user.check_password('test_pass'))
