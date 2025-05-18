from django.contrib.auth import get_user_model
from django.forms import Form
from django.test import TestCase
from django.urls import reverse

from articles.models import Article
from articles.tests.utils import TestUtils


class ArticleDeleteTestCase(TestCase):
    """

    """
    # URLs
    LOGIN_URL = reverse('login')
    ARTICLE_LIST_URL = reverse('article_list')
    ARTICLE_DELETE_URL = reverse(
        viewname='article_delete',
        kwargs={
            'pk': 1
        }
    )

    # Utility methods
    utils = TestUtils()

    @classmethod
    def setUpTestData(cls):
        """
        Before the execution of all test methods in the 'ArticleDeleteTestCase'
        class, this method is run and set up the test data that all the tests
        will use.

        This method creates a test user and article using the Django ORM.
        These test objects are saved to the database and can be used in the
        tests to ensure that the 'ArticleDeleteView' view is functioning
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

    def test_delete_confirm_render_user_not_authenticated(self):
        """
        This method tests the behavior of the "ArticleDeleteView" view when a
        non-authenticated user tries to access an article delete confirm page.

        It sends an HTTP GET request to the "ArticleDeleteView" view URL and
        verifies that the view redirects to the login page as expected.
        """
        # HTTP Response
        response = self.client.get(
            path=self.ARTICLE_DELETE_URL,
            follow=True
        )

        # Checks that there is a redirect to the login page
        self.utils.check_login_redirect(
            response=response,
            target_url=self.ARTICLE_DELETE_URL
        )

    def test_delete_confirm_render_user_not_authorized(self):
        """
        This method tests the behavior of the "ArticleDeleteView" view when
        an authenticated user tries to access an article delete confirm page
        for an article that is not of their authorship.

        It sends an HTTP GET request to the "ArticleDeleteView" view URL and
        verifies that the server returns an HTTP 403 status code as expected.
        """
        # Log in with the second test user
        self.client.login(
            username='test_user_2',
            password='test_pass'
        )

        # HTTP Response
        response = self.client.get(path=self.ARTICLE_DELETE_URL)

        # Checks that an HTTP 403 (Forbidden) status code is returned.
        self.assertEqual(
            first=response.status_code,
            second=403
        )

    def test_delete_confirm_render_user_authorized(self):
        """
        This method tests the behavior of the "ArticleDeleteView" view when
        an authenticated user tries to access an article delete confirm page
        for an article of their authorship.

        It sends an HTTP GET request to the "ArticleDeleteView" view URL and
        verifies that the view renders the article's deletion confirm form
        as expected.
        """
        # Log in with the first test user
        self.client.login(
            username='test_user',
            password='test_pass'
        )

        # HTTP Response
        response = self.client.get(path=self.ARTICLE_DELETE_URL)

        # Checks that an HTTP 200 (OK) status code is returned.
        self.assertEqual(
            first=response.status_code,
            second=200
        )

        # Checks that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='articles/article_delete.html'
        )

        # Checks that the view sends a 'delete confirm form' in the context
        self.assertIsInstance(
            obj=response.context['form'],
            cls=Form
        )

    def test_delete_confirm_submit_user_not_authenticated(self):
        """
        This method tests the behavior of the "ArticleDeleteView" view when
        a not authenticated user tries to submit an article delete confirmation.

        It sends an HTTP POST request to the "ArticleDeleteView" view URL and
        verifies that the view redirects to the login page as expected.
        """
        # HTTP Response
        response = self.client.post(
            path=self.ARTICLE_DELETE_URL,
            follow=True
        )

        # Checks that there is a redirect to the login page
        self.utils.check_login_redirect(
            response=response,
            target_url=self.ARTICLE_DELETE_URL
        )

        # Checks that the article has not been deleted
        self.assertEqual(
            first=Article.objects.count(),
            second=1
        )

    def test_delete_confirm_submit_user_not_authorized(self):
        """
        This method tests the behavior of the "ArticleDeleteView" view when
        an authenticated user tries to submit an article delete confirmation
        for an article that is not of their authorship.

        It sends an HTTP POST request to the "ArticleDeleteView" view URL and
        verifies that the server returns an HTTP 403 status code as expected.
        """
        # Log in with the second test user
        self.client.login(
            username='test_user_2',
            password='test_pass'
        )

        # HTTP Response
        response = self.client.post(path=self.ARTICLE_DELETE_URL)

        # Checks that an HTTP 403 (Forbidden) status code is returned.
        self.assertEqual(
            first=response.status_code,
            second=403
        )

    def test_delete_confirm_submit_user_authorized(self):
        """
        This method tests the behavior of the "ArticleDeleteView" view when
        an authenticated user tries to submit an article delete confirmation
        for an article that is of their authorship.

        It sends an HTTP POST request to the "ArticleDeleteView" view URL
        and verifies that the view deletes the article and redirects the user
        to the article list page as expected.
        """
        # Log in with the fist test user
        self.client.login(
            username='test_user',
            password='test_pass'
        )

        # HTTP Response
        response = self.client.post(
            path=self.ARTICLE_DELETE_URL,
            follow=True
        )

        # Checks that there is a redirect to the article list page
        self.assertRedirects(
            response=response,
            expected_url=self.ARTICLE_LIST_URL,
            status_code=302,
            target_status_code=200
        )

        # Checks that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='articles/article_list.html'
        )

        # Checks that the article has been deleted
        self.assertEqual(
            first=Article.objects.count(),
            second=0
        )
