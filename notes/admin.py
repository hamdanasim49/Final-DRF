from django.contrib import admin

from notes.models import Comment
from notes.models import Note
from notes.models import NoteVersion
from notes.models import Tag

# Register your models here.
admin.site.register(Note)
admin.site.register(Comment)
admin.site.register(NoteVersion)
admin.site.register(Tag)
