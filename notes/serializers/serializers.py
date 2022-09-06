from operator import index
from django.db import models
from ..models import Note
from users.models import User
from rest_framework import serializers


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for Notes and all of its CRUD
    operations and serializing the data
    """

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "text",
            "user",
            "date_created",
            "date_updated",
            "shared_with",
            "archive",
        ]
        indexes = [
            models.Index(fields=["date_updated", "-date_created"]),
        ]

    def create(self, validated_data):
        user = validated_data.pop("user")
        title = validated_data.pop("title")
        text = validated_data.pop("text")

        instance = Note.objects.create(
            user=user, title=title, text=text, **validated_data
        )
        return instance
