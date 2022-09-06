from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    This class represents an instance of user. A user
    consists of first and last name, a unique username,
    a password and an email
    """

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=40)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username
