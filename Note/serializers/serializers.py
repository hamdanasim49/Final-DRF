from operator import index
from django.db import models
from ..models import Note
from User.models import User
from rest_framework import serializers


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for Notes and all of its CRUD
    operations and serializing the data
    """

    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "text",
            "date_created",
            "date_updated",
            "shared_with",
            "archive",
        ]
        indexes = [
            models.Index(fields=["date_updated", "-date_created"]),
        ]

    def update(self, instance, validated_data):
        """Check if update command have title in body then validate it and
        update the data"""
        if "title" in validated_data:
            instance.title = validated_data["title"]
        """Check if update command have text in body then validate it and
        update the data"""
        if "text" in validated_data:
            instance.text = validated_data["text"]

        """Check if body have shared with in parameter then get the list of users
        and add it to the shared with of the user"""
        if "shared_with" in validated_data:
            shared_with_Data = validated_data["shared_with"]
            if shared_with_Data:
                for user in shared_with_Data:
                    if user.id != instance.user.id:
                        curUser = User.objects.get(id=user.id)
                        instance.shared_with.add(curUser.id)
        if "archive" in validated_data:
            instance.archive = validated_data["archive"]

        instance.save()
        return instance
