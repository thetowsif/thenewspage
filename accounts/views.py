from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import CustomUserCreationForm


class SignUpView(UserPassesTestMixin, CreateView):
    """
    A class-based view that inherits from Django generic 'CreateView' view
    and uses the 'UserPassesTestMixin' mixin and implements the user signup
    logic exclusively for non-authenticated users.

    Attributes:
        * form_class: Class-based form to use in the user signup process.
        * success_url: URL for a successful signup process.
        * template_name: Signup form template name.
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def test_func(self):
        """
        A method that implements the user validation logic before allowing
        registration.
        In this case, it checks if the current user has not been
        authenticated.
        :return: True if the current user has not been authenticated.
        False otherwise.
        """
        return not self.request.user.is_authenticated
