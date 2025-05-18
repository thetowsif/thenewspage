from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class LogoutTestCase(TestCase):
    """
    A unit test case for the default logout behavior in Django, which is
    included in the 'auth' package.
    """
    LOGOUT_URL = reverse('logout')
    HOMEPAGE_URL = reverse('home')

    @classmethod
    def setUpTestData(cls):
        """
        This method creates objects in a test database that are available to
        all unit tests. It is called only once for this test case, and the
        created objects are shared among all unit tests in this test case.
        """
        # Custom user model used by this project
        user_model = get_user_model()

        # Test user
        cls.user = user_model.objects.create_user(
            username='test_user',
            password='test_pass',
            email='test@example.net',
            age=18
        )

    def test_logout_user_not_authenticated(self):
        """
        Checks that the logout logic for non-authenticated users results in a
        redirect to the website homepage.
        """
        # HTTP Response
        response = self.client.get(
            path=self.LOGOUT_URL,
            follow=True
        )

        # Checks that there is a redirect to the website homepage
        self.assertRedirects(
            response=response,
            expected_url=self.HOMEPAGE_URL,
            status_code=302,
            target_status_code=200
        )

        # Checks that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='home.html'
        )

    def test_logout_user_authenticated(self):
        """
        Checks that the logout logic for authenticated users results in a
        redirect to the website homepage and close the active session.
        """
        self.client.login(
            username='test_user',
            password='test_pass'
        )

        # HTTP Response
        response = self.client.get(
            path=self.LOGOUT_URL,
            follow=True
        )

        # Checks that the user session has been closed
        self.assertFalse(
            expr=response.context['user'].is_authenticated
        )

        # Checks that there is a redirect to the website homepage
        self.assertRedirects(
            response=response,
            expected_url=self.HOMEPAGE_URL,
            status_code=302,
            target_status_code=200
        )

        # Checks that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='home.html'
        )
