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

    def update(self, instance, validated_data):
        super().update(instance, validated_data)

        """Check if body have shared with in parameter then get the list of users
        and add it to the shared with of the user"""
        if "shared_with" in validated_data:
            shared_with_data = validated_data["shared_with"]
            if shared_with_data:
                print(shared_with_data)
                for user in shared_with_data:
                    if user.id != instance.user.id:
                        curUser = User.objects.get(id=user.id)
                        instance.shared_with.add(curUser.id)

        instance.save()
        return instance
