from factory.django import DjangoModelFactory
from notes.models import Note
from users.tests.factory import UserFactory


class NoteFactory(DjangoModelFactory):
    """Factory class to create User objects."""

    class Meta:
        model = Note

    title = "This is a test title"
    text = "This is a test text"
