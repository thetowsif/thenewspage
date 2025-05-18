from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from articles.forms import CommentForm
from articles.models import Article, Comment
from articles.tests.utils import TestUtils


class ArticleDetailTestCase(TestCase):
    """
    A Django 'TestCase' subclass that contains unit tests for the
    'ArticleDetailView' view.

    These tests ensure that the view follows the proper logic, returning the
    expected HTTP response codes, rendering the correct templates, and
    displaying the details of a specific article.
    """
    # URLS
    LOGIN_URL = reverse('login')
    ARTICLE_DETAIL_URL = reverse(
        'article_detail',
        kwargs={
            'pk': 1
        }
    )
    # Utility methods
    utils = TestUtils()

    @classmethod
    def setUpTestData(cls):
        """
        Before the execution of all test methods in the 'ArticleDetailTestCase'
        class, this method is run and set up the test data that all the tests
        will use.

        This method creates a test user and article using the Django ORM.
        These test objects are saved to the database and can be used in the
        tests to ensure that the 'ArticleListView' view is functioning
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

        # Test article
        Article.objects.create(
            pk=1,
            title='Test Article',
            body='Test Body',
            author=cls.user
        )

    def test_article_details_user_not_authenticated(self):
        """
        This method tests the behavior of the "ArticleDetailView" view for
        non-authenticated users.

        It sends an HTTP GET request to the "ArticleDetailView" URL and verifies
        that the view redirects to the login page as expected. It also checks
        the proper template render.
        """
        # Http Response
        response = self.client.get(
            path=self.ARTICLE_DETAIL_URL,
            follow=True
        )

        # Checks that there is a redirect to the login page
        self.utils.check_login_redirect(
            response=response,
            target_url=self.ARTICLE_DETAIL_URL
        )

    def test_article_detail_user_authenticated(self):
        """
        This method tests the behavior of the "ArticleDetailView" view for
        authenticated users.

        It sends an HTTP GET request to the "ArticleDetailView" URL and verifies
        that the view shows the article detail page as expected.

        It also checks the proper template render and the article and comment
        form included in the view context.
        """
        self.client.login(
            username='test_user',
            password='test_pass'
        )

        # HTTP Response
        response = self.client.get(path=self.ARTICLE_DETAIL_URL)

        # Checks that an HTTP 200 (OK) status code is returned.
        self.assertEqual(
            first=response.status_code,
            second=200
        )

        # Checks that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='articles/article_detail.html'
        )

        # Checks that the view sends the correct 'Article' object in the context
        self.assertEqual(
            first=response.context['article'],
            second=Article.objects.get(pk=1)
        )

        # Checks that the view sends a 'CommentForm' form in the context
        self.assertIsInstance(
            obj=response.context['form'],
            cls=CommentForm
        )

    def test_add_comment_user_not_authenticated(self):
        """
        Checks that non-authenticated users are redirected to the login page
        when attempting to add a comment to an article.

        This test sends an HTTP POST request to the "ArticleDetailView" URL
        with comment data for a non-authenticated user and verifies that
        there is a redirect to the login page.
        """
        comment_data = {
            'comment': 'some comment'
        }

        # HTTP Response
        response = self.client.post(
            path=self.ARTICLE_DETAIL_URL,
            data=comment_data,
            follow=True
        )

        self.utils.check_login_redirect(
            response=response,
            target_url=self.ARTICLE_DETAIL_URL
        )

    def test_add_valid_comment_user_authenticated(self):
        """
        Checks that authenticated users can add valid comments to an article.

        This test logs with an authenticated user and send an HTTP POST request
        to the "ArticleDetailView" URL with valid comment data.
        """
        self.client.login(
            username='test_user',
            password='test_pass'
        )

        comment_data = {
            'comment': 'some valid comment'
        }

        # HTTP Response
        response = self.client.post(
            path=self.ARTICLE_DETAIL_URL,
            data=comment_data,
            follow=True
        )

        # Checks that there is a redirect to the article detail page
        self.assertRedirects(
            response=response,
            expected_url=self.ARTICLE_DETAIL_URL,
            status_code=302,
            target_status_code=200
        )

        # Checks that the comment is saved in the database
        self.assertEqual(
            first=Comment.objects.count(),
            second=1
        )

        # Checks that the comment author is the current logged user
        user_model = get_user_model()
        self.assertEqual(
            first=Comment.objects.get(pk=1).author,
            second=user_model.objects.get(username='test_user')
        )

        # Checks that the commented article is the correct
        self.assertEqual(
            first=Comment.objects.get(pk=1).article,
            second=Article.objects.get(pk=1)
        )

        # Checks that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='articles/article_detail.html'
        )

        # Checks that the comment is render properly
        self.assertContains(
            response=response,
            text='some valid comment'
        )

    def test_add_invalid_comment_user_authenticated(self):
        """
        Checks that authenticated users cannot add invalid comments
        to an article.

        This test logs with an authenticated user and send an HTTP POST request
        to the "ArticleDetailView" URL with invalid comment data.
        """
        self.client.login(
            username='test_user',
            password='test_pass'
        )

        invalid_comment_data = {
            'comment': ''
        }

        # HTTP Response
        response = self.client.post(
            path=self.ARTICLE_DETAIL_URL,
            data=invalid_comment_data
        )

        # Checks that an HTTP 200 (OK) status code is returned.
        self.assertEqual(
            first=response.status_code,
            second=200
        )

        # Checks that the view sends the correct 'Article' object in the context
        self.assertEqual(
            first=response.context['article'],
            second=Article.objects.get(pk=1)
        )

        # Checks that the view sends a 'CommentForm' form in the context
        self.assertIsInstance(
            obj=response.context['form'],
            cls=CommentForm
        )

        # Checks that the comment form has errors
        self.assertTrue(
            expr=response.context['form'].errors
        )

        # Checks that the comment form has an error in the 'comment' field
        self.assertIn(
            member='comment',
            container=response.context['form'].errors
        )
