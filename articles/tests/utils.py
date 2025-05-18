from django.test import TestCase
from django.urls import reverse


class TestUtils(TestCase):
    """
    A utility class for the Django project unit tests.

    This class extends the Django 'TestCase' class and provides utility methods
    available for multiple test cases.
    """
    LOGIN_URL = reverse('login')

    def check_login_redirect(self, response, target_url):
        """
        Check that the given response redirects to the login page for the
        specified target URL.

        :param response: The HTTP response.
        :param target_url: The target URL to redirect to after successful login.
        """
        redirect_url = f'{self.LOGIN_URL}?next={target_url}'
        self.assertRedirects(
            response=response,
            expected_url=redirect_url,
            status_code=302,
            target_status_code=200
        )
        self.assertTemplateUsed(
            response=response,
            template_name='registration/login.html'
        )
