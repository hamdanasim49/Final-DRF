import json

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from notes.models import Note
from notes.serializers.serializers import NoteSerializer


class Command(BaseCommand):
    """
    This is a admin command class that will enable us to
    write custom commands for admin
    """

    def handle(self, *args, **options):
        archive_notes = Note.objects.all().filter(archive=True)
        for note in archive_notes:
            self.stdout.write(str(note.id) + "\t" + note.title + "\t" + note.text)
