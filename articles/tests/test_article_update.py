from django.contrib.auth import get_user_model
from django.forms import ModelForm, model_to_dict
from django.test import TestCase
from django.urls import reverse

from articles.models import Article
from articles.tests.utils import TestUtils


class ArticleUpdateTestCase(TestCase):
    """
    A Django 'TestCase' subclass that contains unit tests for the
    'ArticleUpdateView' view.

    These tests ensure that the view follows the proper logic, returning
    the expected HTTP response codes, rendering the correct templates, and
    allowing an article edition.
    """
    # URLs
    LOGIN_URL = reverse('login')
    ARTICLE_UPDATE_URL = reverse(
        viewname='article_edit',
        kwargs={
            'pk': 1
        }
    )
    ARTICLE_DETAIL_URL = reverse(
        viewname='article_detail',
        kwargs={
            'pk': 1
        }
    )

    # Utility methods
    utils = TestUtils()

    @classmethod
    def setUpTestData(cls):
        """
        Before the execution of all test methods in the 'ArticleUpdateTestCase'
        class, this method is run and set up the test data that all the tests
        will use.

        This method creates a test user and article using the Django ORM.
        These test objects are saved to the database and can be used in the
        tests to ensure that the 'ArticleUpdateView' view is functioning
        correctly.
        """
        # Project custom user model
        user_model = get_user_model()

        # Test user
        cls.user = user_model.objects.create_user(
            username='test_user',
            password='test_pass',
            email='test@example.net',
            age=18
        )

        cls.user_2 = user_model.objects.create_user(
            username='test_user_2',
            password='test_pass',
            email='test2@example.net',
            age=81
        )

        # Test article
        cls.test_article = Article.objects.create(
            pk=1,
            title='Test Article',
            body='Test Body',
            author=cls.user
        )

    def test_update_form_render_user_not_authenticated(self):
        """
        This method tests the behavior of the "ArticleUpdateView" view when a
        non-authenticated user tries to access an article update form.

        It sends an HTTP GET request to the "ArticleUpdateView" view URL and
        verifies that the view redirects to the login page as expected.
        """
        # HTTP Response
        response = self.client.get(
            path=self.ARTICLE_UPDATE_URL,
            follow=True
        )

        # Checks that there is a redirect to the login page
        self.utils.check_login_redirect(
            response=response,
            target_url=self.ARTICLE_UPDATE_URL
        )

    def test_update_form_render_user_unauthorized(self):
        """
        This method tests the behavior of the "ArticleUpdateView" view when an
        authenticated user tries to access the update form for an article that
        is not of their authorship.

        It sends an HTTP GET request to the "ArticleUpdateView" view URL and
        verifies that the server returns an HTTP 403 status code as expected.
        """
        # Log in with the second test user
        self.client.login(
            username='test_user_2',
            password='test_pass'
        )

        # HTTP Response
        response = self.client.get(path=self.ARTICLE_UPDATE_URL)

        # Checks that an HTTP 403 (Forbidden) status code is returned.
        self.assertEqual(
            first=response.status_code,
            second=403
        )

    def test_update_form_render_user_authorized(self):
        """
        This method tests the behavior of the "ArticleUpdateView" view when an
        authenticated user access the update form for an article that is of
        their authorship.

        It sends an HTTP GET request to the "ArticleUpdateView" view URL while
        an authenticated (and authorized) user is logged in and verifies that
        the view returns an HTTP 200 (OK) status code.
        It also checks that the view renders the correct template and sends
        a 'ModelForm' form in the context.
        """
        # Log in with the first test user
        self.client.login(
            username='test_user',
            password='test_pass'
        )

        # HTTP Response
        response = self.client.get(path=self.ARTICLE_UPDATE_URL)

        # Checks that an HTTP 200 (OK) status code is returned.
        self.assertEqual(
            first=response.status_code,
            second=200
        )

        # Checks that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='articles/article_edit.html'
        )

        # Checks that the view sends a 'ModelForm' form in the context
        self.assertIsInstance(
            obj=response.context['form'],
            cls=ModelForm
        )

        # Checks that the article update form includes the correct information
        article_partial_data = model_to_dict(
            instance=self.test_article,
            fields=['title', 'body']
        )
        self.assertEqual(
            first=response.context['form'].initial,
            second=article_partial_data
        )

    def test_update_form_submit_user_not_authenticated(self):
        """
        This method tests the behavior of the "ArticleUpdateView" view when a
        non-authenticated user tries to access an article update form.

        It sends an HTTP GET request to the "ArticleUpdateView" view URL and
        verifies that the view redirects to the login page as expected. It also
        checks that the article has not been modified.
        """
        article_update = {
            'title': 'Updated title',
            'body': 'Updated Body'
        }

        # HTTP Response
        response = self.client.post(
            path=self.ARTICLE_UPDATE_URL,
            data=article_update,
            follow=True
        )

        # Checks that there is a redirect to the login page
        self.utils.check_login_redirect(
            response=response,
            target_url=self.ARTICLE_UPDATE_URL
        )

        # Checks that the article has not been modified
        self.test_article.refresh_from_db()  # Updated test article
        self.assertNotEqual(
            first=self.test_article,
            second=article_update
        )

    def test_update_form_submit_user_not_authorized(self):
        """
        This method tests the behavior of the "ArticleUpdateView" view when an
        authenticated user tries to submit the update form of an article that
        is not of their authorship.

        It sends an HTTP POST request to the "ArticleUpdateView" view URL and
        verifies that the server returns an HTTP 403 status code as expected.
        """
        # Log in with the second test user
        self.client.login(
            username='test_user_2',
            password='test_pass'
        )

        article_update = {
            'title': 'Updated title',
            'body': 'Updated Body'
        }

        # HTTP Response
        response = self.client.post(
            path=self.ARTICLE_UPDATE_URL,
            data=article_update
        )

        # Checks that an HTTP 403 (Forbidden) status code is returned.
        self.assertEqual(
            first=response.status_code,
            second=403
        )

    def test_invalid_update_form_submit_user_authorized(self):
        """
        This method tests the behavior of the "ArticleUpdateView" view when an
        authenticated user tries to submit the update form of an article that
        is of their authorship with invalid data.

        It sends an HTTP POST request to the "ArticleUpdateView" view URL
        and verifies that the view renders the update form template, showing
        the errors in their respective fields.
        """
        # Log in with the first test user
        self.client.login(
            username='test_user',
            password='test_pass'
        )

        article_update = {
            'title': '',
            'body': 'Updated Body'
        }

        # HTTP Response
        response = self.client.post(
            path=self.ARTICLE_UPDATE_URL,
            data=article_update
        )

        # Checks that an HTTP 200 (OK) status code is returned.
        self.assertEqual(
            first=response.status_code,
            second=200
        )

        # Checks that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='articles/article_edit.html'
        )

        # Checks that the view sends a 'ModelForm' form in the context
        self.assertIsInstance(
            obj=response.context['form'],
            cls=ModelForm
        )

        # Checks that the article update form has errors
        self.assertTrue(
            expr=response.context['form'].errors
        )

        # Checks that the article update form has an error in the 'title' field
        self.assertIn(
            member='title',
            container=response.context['form'].errors
        )

        # Checks that the article has not been modified
        self.test_article.refresh_from_db()  # Updated test article
        self.assertNotEqual(
            first=self.test_article,
            second=article_update
        )

    def test_update_form_submit_user_authorized(self):
        """
        This method tests the behavior of the "ArticleUpdateView" view when
        an authenticated user tries to submit the update form of an article
        that is of their authorship with valid data.

        It sends an HTTP POST request to the "ArticleUpdateView" view URL and
        checks that the view redirects to the article detail page, renders
        the appropriate template, and saves the article updates into the
        database.
        """
        # Log in with the first test user
        self.client.login(
            username='test_user',
            password='test_pass'
        )

        article_update = {
            'title': 'Updated Title',
            'body': 'Updated Body'
        }

        # HTTP Response
        response = self.client.post(
            path=self.ARTICLE_UPDATE_URL,
            data=article_update,
            follow=True
        )

        # Checks that there is a redirect to the article detail page
        self.assertRedirects(
            response=response,
            expected_url=self.ARTICLE_DETAIL_URL,
            status_code=302,
            target_status_code=200
        )

        # Checks that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='articles/article_detail.html'
        )

        # Checks that the article has been modified
        self.test_article.refresh_from_db()
        article_partial_data = model_to_dict(
            instance=self.test_article,
            fields=['title', 'body']
        )

        self.assertEqual(
            first=article_partial_data,
            second=article_update
        )

        # Checks that the article instance is included in the context
        self.assertEqual(
            first=response.context['article'],
            second=self.test_article
        )
