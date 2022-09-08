from django.contrib import admin
from notes.models import Note, Comment, NoteVersion

# Register your models here.
admin.site.register(Note)
admin.site.register(Comment)
admin.site.register(NoteVersion)
