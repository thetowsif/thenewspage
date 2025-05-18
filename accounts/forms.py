from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    A custom user signup class-based form that extends the Django
    UserCreationForm class, adding a user age field.
    """
    class Meta:
        """
        That is the Meta class for the CustomUserCreationForm class-based form
        that allows the specification of additional options referred to as meta
        attributes.

        Attributes:
            model: The base model for this form.
            fields: The fields that this form should include.
        """
        model = CustomUser
        fields = (
            'username',
            'email',
            'age'
        )


class CustomUserChangeForm(UserChangeForm):
    """
    Custom user edit class-based form that extends the Django UserChangeForm
    class, adding a user age field.
    """
    class Meta:
        """
        That is the Meta class for the CustomUserChangeForm class-based form
        that allows the specification of additional options referred to as
        meta attributes.

        Attributes:
            model: The base model for this form.
            fields: The fields that this form should include.
        """
        model = CustomUser
        fields = (
            'username',
            'email',
            'age'
        )
