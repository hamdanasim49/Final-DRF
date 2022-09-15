from django.db import models
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

from ..models import Comment
from ..models import Note
from ..models import NoteVersion
from notes import constant
from users.models import User
from users.serializers.serializers import UserSerializer


class SingleCommentSerializer(serializers.ModelSerializer):
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

    comments = SingleCommentSerializer(many=True, read_only=True)

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
            "archive",
        ]
        indexes = [
            models.Index(fields=["date_updated", "-date_created"]),
        ]
        extra_kwargs = {"title": {"required": True}, "text": {"required": True}}
        ordering = ["-id"]

    def update(self, instance, validated_data):
        if self.context.get("request") != None and self.context["request"].user:
            user = self.context["request"].user
            NoteVersion.objects.create(
                note_id=instance,
                title=instance.title,
                text=instance.text,
                edited_by=user,
                date_created=instance.date_created,
                date_updated=instance.date_updated,
            )
            return super().update(instance, validated_data)
        else:
            raise serializers.ValidationError(
                {"request": "Context have no key named request"}
            )

    def to_representation(self, instance):
        """
        Overriding this function to just show the latest comment if we list
        down all the notes of a user
        """

        representation = super().to_representation(instance)
        representation["comments"] = CommentSerializer(
            instance.comments.all().last()
        ).data
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
        paginator.page_size = constant.PAGE_SIZE
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

    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        ordering = ["-id"]

    def create(self, validated_data):
        note = validated_data.pop("note")
        text = validated_data.pop("text")

        instance = Comment.objects.create(
            user=self.context["request"].user, note=note, text=text, **validated_data
        )
        return instance
