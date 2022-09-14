from factory.django import DjangoModelFactory
from faker import Factory

from notes.models import Note
from users.tests.factory import UserFactory

faker = Factory.create()


class NoteFactory(DjangoModelFactory):
    """Factory class to create User objects."""

    class Meta:
        model = Note

    title = faker.text()
    text = faker.text()
