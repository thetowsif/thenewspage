from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model that extends the Django 'AbstractUser' class and adds an
    age field to the default fields inherited from this superclass.

    Attributes:
        * age: An optional field for storing the user's age as a positive
        integer value.
    """
    age = models.PositiveIntegerField(
        null=True,
        blank=True
    )
