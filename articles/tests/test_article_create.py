from django.contrib.auth import get_user_model
from django.forms import ModelForm, model_to_dict
from django.test import TestCase
from django.urls import reverse

from articles.models import Article
from articles.tests.utils import TestUtils


class ArticleCreateTestCase(TestCase):
    """
    A Django 'TestCase' subclass that contains unit tests for the
    'ArticleCreateView' view.

    These tests ensure that the view follows the proper logic, returning
    the expected HTTP response codes, rendering the correct templates, and
    allowing new article creation.
    """
    # URLs
    LOGIN_URL = reverse('login')
    NEW_ARTICLE_URL = reverse('article_new')
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
        Before the execution of all test methods in the 'ArticleCreateTestCase'
        class, this method is run and set up the test data that all the tests
        will use.

        This method creates a test user and article using the Django ORM.
        These test objects are saved to the database and can be used in the
        tests to ensure that the 'ArticleCreateView' view is functioning
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

    def test_create_form_render_user_not_authenticated(self):
        """
        This method tests the behavior of the "ArticleCreateView" view for
        non-authenticated users.

        It sends an HTTP GET request to the "ArticleCreateView" view URL and
        verifies that the view redirects to the login page as expected.
        It also checks the proper template render.
        """
        # HTTP Response
        response = self.client.get(
            path=self.NEW_ARTICLE_URL,
            follow=True
        )

        # Checks that there is a redirect to the login page
        self.utils.check_login_redirect(
            response=response,
            target_url=self.NEW_ARTICLE_URL
        )

    def test_create_form_render_user_authenticated(self):
        """
        This method tests the behavior of the "ArticleCreateView" view for
        authenticated users.

        It sends an HTTP GET request to the "ArticleCreateView" view URL while
        an authenticated user is logged in and verifies that the view returns an
        HTTP 200 (OK) status code. It also checks that the view renders the
        correct template and sends a 'ModelForm' form in the context.
        """

        self.client.login(
            username='test_user',
            password='test_pass'
        )

        # HTTP Response
        response = self.client.get(path=self.NEW_ARTICLE_URL)

        # Checks that an HTTP 200 (OK) status code is returned.
        self.assertEqual(
            first=response.status_code,
            second=200
        )

        # Checks that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='articles/article_new.html'
        )

        # Checks that the view sends a 'CommentForm' form in the context
        self.assertIsInstance(
            obj=response.context['form'],
            cls=ModelForm
        )

    def test_create_form_submit_user_not_authenticated(self):
        """
        This method tests the behavior of the "ArticleCreateView" view
        when a non-authenticated user submits a form to create a new article.

        It sends an HTTP POST request to the "ArticleCreateView" view URL with
        the new article data and verifies that the view redirects to the login
        page as expected. It also checks that there are no new articles
        in the database.
        """

        new_article_data = {
            'title': 'A new article',
            'body': 'Article Body'
        }

        # HTTP Response
        response = self.client.post(
            path=self.NEW_ARTICLE_URL,
            data=new_article_data,
            follow=True
        )

        # Checks that there is a redirect to the login page
        self.utils.check_login_redirect(
            response=response,
            target_url=self.NEW_ARTICLE_URL
        )

        # Checks that no articles were saved to the database
        self.assertEqual(
            first=Article.objects.count(),
            second=0
        )

    def test_create_form_submit_user_authenticated(self):
        """
        This method tests the behavior of the "ArticleCreateView" view
        when an authenticated user submits a form to create a new article.

        It sends an HTTP POST request to the "ArticleCreateView" view URL with
        the new article data and verifies that the view redirects to the article
        details page as expected. It also checks that there is a new article
        in the database.
        """
        self.client.login(
            username='test_user',
            password='test_pass'
        )

        new_article_data = {
            'title': 'A new article',
            'body': 'Article Body'
        }

        # HTTP Response
        response = self.client.post(
            path=self.NEW_ARTICLE_URL,
            data=new_article_data,
            follow=True
        )

        # Checks that there is a redirect to the article detail page
        self.assertRedirects(
            response=response,
            expected_url=self.ARTICLE_DETAIL_URL,
            status_code=302,
            target_status_code=200
        )

        # Checks that the article was saved in the database
        self.assertEqual(
            first=Article.objects.count(),
            second=1
        )

        # Checks that the created article contains the correct form data
        article = Article.objects.get(pk=1)
        article_partial_data = model_to_dict(
            instance=article,
            fields=['title', 'body']
        )

        self.assertEqual(
            first=article_partial_data,
            second=new_article_data
        )

        # Checks that the article author is the currently authenticated user
        self.assertEqual(
            first=article.author,
            second=self.user
        )

        # Checks that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='articles/article_detail.html'
        )

        # Checks that the view sends the correct 'Article' object in the context
        self.assertEqual(
            first=response.context['article'],
            second=article
        )

    def test_create_form_invalid_submit_user_authenticated(self):
        """
        This method tests the behavior of the "ArticleCreateView" view when
        an authenticated user submits a form to create a new article
        with invalid data.

        It sends an HTTP POST request to the "ArticleCreateView" view URL
        with the new article's invalid data and verifies that the view
        shows the article creation form with error messages. It also checks
        that there are no new articles in the database.
        """
        self.client.login(
            username='test_user',
            password='test_pass'
        )

        new_article_data = {
            'title': 'A new article',
            'body': ''
        }

        # HTTP Response
        response = self.client.post(
            path=self.NEW_ARTICLE_URL,
            data=new_article_data
        )

        # Checks that an HTTP 200 (OK) status code is returned.
        self.assertEqual(
            first=response.status_code,
            second=200
        )

        # Checks that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='articles/article_new.html'
        )

        # Checks that the view sends a 'ModelForm' form in the context
        self.assertIsInstance(
            obj=response.context['form'],
            cls=ModelForm
        )

        # Checks that the form contains errors
        self.assertTrue(
            expr=response.context['form'].errors
        )

        # Checks that the form contains an error in the 'body' field
        self.assertIn(
            member='body',
            container=response.context['form'].errors
        )

        # Checks that no article was saved to the database
        self.assertEqual(
            first=Article.objects.count(),
            second=0
        )
