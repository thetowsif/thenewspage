from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from articles.models import Article
from articles.tests.utils import TestUtils


class ArticleListTestCase(TestCase):
    """
    A Django 'TestCase' subclass that contains unit tests for the
    "ArticleListView" view.

    These tests ensure that the view follows the proper logic, returning the
    expected HTTP response codes, rendering the correct templates, and
    displaying the list of available articles in the database.
    """
    # URLs
    LOGIN_URL = reverse('login')
    ARTICLE_LIST_URL = reverse('article_list')

    # Utility methods
    utils = TestUtils()

    @classmethod
    def setUpTestData(cls):
        """
        Before the execution of all test methods in the 'ArticleListTestCase'
        class, this method is run and set up the test data that all the tests
        will use.

        This method creates a test user and several test articles using
        the Django ORM. These test objects are saved to the database and can
        be used in the tests to ensure that the 'ArticleListView' view
        is functioning correctly.
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

        # Test articles
        Article.objects.create(
            title='Test Article 1',
            body='Test Body 1',
            author=cls.user
        )

        Article.objects.create(
            title='Test Article 2',
            body='Test Body 2',
            author=cls.user
        )

        Article.objects.create(
            title='Test Article 3',
            body='Test Body 3',
            author=cls.user
        )

    def test_article_list_render_user_not_authenticated(self):
        """
        This method tests the behavior of the "ArticleListView" view for
        non-authenticated users.

        It sends an HTTP GET request to the "ArticleListView" URL and verifies
        that the view redirects to the login page as expected. It also checks
        the proper template render.
        """
        # HTTP response
        response = self.client.get(
            path=self.ARTICLE_LIST_URL,
            follow=True
        )

        # Checks that there is a redirect to the login page
        self.utils.check_login_redirect(
            response=response,
            target_url=self.ARTICLE_LIST_URL
        )

    def test_article_list_render_user_authenticated(self):
        """
        It is a method that tests the behavior of the "ArticleListView" view
        for authenticated users.

        This method logs in with the test user, sends an HTTP GET request to
        the "ArticleListView" URL, and verifies that the view returns an
        HTTP 200 (OK) status code. It also checks that the full articles list
        is sent in the context and the proper template rendering.
        """
        self.client.login(
            username='test_user',
            password='test_pass'
        )

        # HTTP Response
        response = self.client.get(
            path=self.ARTICLE_LIST_URL,
            follow=True
        )

        # Checks that an HTTP 200 (OK) status code is returned.
        self.assertEqual(
            first=response.status_code,
            second=200
        )

        # Checks that the view sends the full articles list in the context.
        self.assertQuerysetEqual(
            qs=response.context['article_list'],
            values=Article.objects.all(),
            ordered=False
        )

        # Checks that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='articles/article_list.html'
        )
