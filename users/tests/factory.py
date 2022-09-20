from factory.django import DjangoModelFactory
from faker import Factory

from users.models import User

faker = Factory.create()


class UserFactory(DjangoModelFactory):
    """Factory class to create User objects."""

    class Meta:
        model = User

    email = faker.email()
    first_name = faker.name()
    last_name = faker.name()
    username = faker.profile(fields=["username"])["username"]
