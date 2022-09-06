from django.db import models
from users.models import User


class Note(models.Model):
    """
    This class is Notes model which will be the information that we
    will be storing about notes in our db
    """

    title = models.CharField(max_length=20, default=" ")
    text = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    archive = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    shared_with = models.ManyToManyField(
        User, related_name="Shared_notes_user", blank=True
    )

    def __str__(self):
        return self.text + "  " + self.user.username
