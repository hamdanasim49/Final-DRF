from django.db import models

from users.models import User


class AbstractModel(models.Model):
    """
    An abstract class that will contain 2 attributes that are date created and
    date updated
    """

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Note(AbstractModel):
    """
    This class is Notes model which will be the information that we
    will be storing about notes in our db
    """

    title = models.CharField(max_length=31)
    text = models.TextField()
    archive = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(
        User, related_name="Shared_notes_user", blank=True
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.text + "  " + self.user.username


class Comment(AbstractModel):
    """
    This class is for Comment model which will be the info that we will store in our
    database, it will have foreign key for user and note as well as body of content
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return str(self.user.id) + " " + self.text


class NoteVersion(AbstractModel):
    """
    This model is used to store all the versions of a specific note.
    versions will basically be history of the edits performed on the Note model
    """

    note_id = models.ForeignKey(Note, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.note_id.id) + " " + self.title + " " + self.text
