from rest_framework.pagination import PageNumberPagination
from django.db import models
from ..models import Note, NoteVersion, Comment
from users.models import User
from rest_framework import serializers
from users.serializers.serializers import UserSerializer


class CommentOneSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model, It is another serializer that will just display
    limited data
    """

    class Meta:
        model = Comment
        fields = ["note_id", "date_updated", "user", "text"]
        ordering = ["-id"]


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for Notes and all of its CRUD
    operations and serializing the data
    """

    comments = CommentOneSerializer(many=True, read_only=True)

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Note
        fields = [
            "id",
            "user",
            "date_created",
            "date_updated",
            "title",
            "text",
            "shared_with",
            "comments",
        ]
        indexes = [
            models.Index(fields=["date_updated", "-date_created"]),
        ]
        extra_kwargs = {"title": {"required": True}, "text": {"required": True}}
        ordering = ["-id"]

    def update(self, instance, validated_data):
        NoteVersion.objects.create(
            note_id=instance,
            title=instance.title,
            text=instance.text,
            edited_by=self.context["request"].user,
            date_created=instance.date_created,
            date_updated=instance.date_updated,
        )

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """
        Overriding this function to just show the latest comment if we list
        down all the notes of a user
        """

        representation = super().to_representation(instance)
        if representation["comments"]:
            if len(representation["comments"]) > 1:
                last_comment = representation["comments"][
                    len(representation["comments"]) - 1
                ]
                representation["comments"] = []
                representation["comments"].append(last_comment)
        return representation


class ObjectNoteSerializer(serializers.ModelSerializer):
    """
    This serializer will work when we will get an object of note
    it will show all the comments of the note in paginated way
    """

    comments = serializers.SerializerMethodField("paginated_comments")

    class Meta:
        model = Note
        fields = "__all__"
        ordering = ["-id"]

    def paginated_comments(self, obj):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        queryset = obj.comments.all()
        result_page = paginator.paginate_queryset(queryset, self.context["request"])
        data = CommentSerializer(result_page, many=True)
        return data.data


class NoteVersionSerializer(serializers.ModelSerializer):
    """
    Serializer for Note version model, it will enable us to
    create and retrieve the versions of notes
    """

    class Meta:
        model = NoteVersion
        fields = "__all__"
        ordering = ["-id"]


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model, It will enable us to create and retrieve
    the comments of a particular note
    """

    class Meta:
        model = Comment
        fields = "__all__"
        note = NoteSerializer()
        user = UserSerializer()
        ordering = ["-id"]

    def create(self, validated_data):
        note = validated_data.pop("note")
        text = validated_data.pop("text")

        instance = Comment.objects.create(
            user=self.context["request"].user, note=note, text=text, **validated_data
        )
        return instance
