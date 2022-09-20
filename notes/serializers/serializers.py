from django.db import models
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

from ..models import Comment
from ..models import Note
from ..models import NoteVersion
from ..models import Tag
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


class TagSerializer(serializers.ModelSerializer):
    """
    A serializer for tag, it will just be used to serialize the
    tag objects of a note
    """

    class Meta:
        model = Tag
        fields = "__all__"


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for Notes and all of its CRUD
    operations and serializing the data
    """

    comments = SingleCommentSerializer(many=True, read_only=True)

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), default=serializers.CurrentUserDefault()
    )
    tags = serializers.ListSerializer(
        child=serializers.CharField(min_length=0, max_length=32)
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
            "tags",
        ]
        indexes = [
            models.Index(fields=["date_updated", "-date_created"]),
        ]
        extra_kwargs = {"title": {"required": True}, "text": {"required": True}}
        ordering = ["-id"]

    def create(self, validated_data):
        """
        This is the create function of serializer in this we first check whether our user exists
        if it do exists then we get the tag object list and assign corresponding values
        """

        if self.context.get("request") is None and not self.context["request"].user:
            raise serializers.ValidationError(
                {"request": "Context have no key named request"}
            )

        tag_name = NoteSerializer.create_tags(validated_data)
        note = Note.objects.create(
            text=validated_data["text"],
            title=validated_data["title"],
            user=self.context["request"].user,
        )
        note.tags.set(tag_name)
        note.save()
        return note

    def update(self, instance, validated_data):
        """
        This is the update function of serializer in this we first check whether our user exists
        if it do exists then we get the tag object list and assign corresponding values
        We also create an object for versioning of note in this
        """

        if self.context.get("request") is None and not self.context["request"].user:
            raise serializers.ValidationError(
                {"request": "Context have no key named request"}
            )
        user = self.context["request"].user
        if "tags" in validated_data:
            tag_name = NoteSerializer.create_tags(validated_data)
            instance.tags.set(tag_name)
            validated_data.pop("tags")
            instance.save()
        NoteVersion.objects.create(
            note_id=instance,
            title=instance.title,
            text=instance.text,
            edited_by=user,
        )
        return super().update(instance, validated_data)

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

    def create_tags(validated_data):
        """
        create_tags : Create tags in db if any particular tag does not exists
        """
        tags_in_db = list(
            Tag.objects.filter(name__in=validated_data["tags"]).values_list(
                "name", flat=True
            )
        )
        tags_not_in_db = list(set(validated_data["tags"]) - set(tags_in_db))
        tags_list = [Tag(name=tag) for tag in tags_not_in_db]
        Tag.objects.bulk_create(tags_list, ignore_conflicts=True)
        tag_names = Tag.objects.filter(name__in=validated_data["tags"]).values_list(
            "name", flat=True
        )
        return tag_names


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
