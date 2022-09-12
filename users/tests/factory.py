from factory.django import DjangoModelFactory
from factory import Faker
from users.models import User


class UserFactory(DjangoModelFactory):
    """Factory class to create User objects."""

    class Meta:
        model = User

    email = "test@test.com"
    first_name = "Dummy"
    last_name = "Name"
    username = "dummyname"
