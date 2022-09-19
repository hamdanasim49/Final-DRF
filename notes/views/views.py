from django_filters import rest_framework as rest_filters
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models import Comment
from ..models import Note
from ..models import NoteVersion
from ..serializers.serializers import CommentSerializer
from ..serializers.serializers import NoteSerializer
from ..serializers.serializers import NoteVersionSerializer
from ..serializers.serializers import ObjectNoteSerializer
from notes.filters.filters import NotesFilter
from notes.permissions.permissions import UserPermission
from project import utilities


class NotesViewsets(viewsets.ModelViewSet):
    """
    Viewset for notes model and it is responsible for all the CRUD operations of
    the notes class.
    """

    queryset = Note.objects.select_related("user").prefetch_related("comments")
    authentication_classes = (JWTAuthentication,)
    serializer_class = NoteSerializer

    pagination_class = PageNumberPagination
    permission_classes = [UserPermission]

    filter_backends = [
        filters.SearchFilter,
        rest_filters.DjangoFilterBackend,
    ]
    filterset_fields = ("archive",)
    search_fields = ["text"]
    filterset_class = NotesFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ObjectNoteSerializer
        return NoteSerializer

    """
    #TODO: We will move this functionality into filters
    """

    def get_queryset(self):
        queryset_current_user_notes = self.queryset.filter(user=self.request.user)
        queryset_shared_notes = Note.objects.filter(shared_with=self.request.user)
        queryset = (queryset_current_user_notes | queryset_shared_notes).distinct()
        return queryset

    """
    This action will be called with the url : /notes/id/versions
    It is responsible for showing all the versions of a note
    """

    @action(detail=True, methods=["GET"], name="versions")
    def versions(self, request, pk=None):
        queryset = NoteVersion.objects.all()
        queryset = queryset.filter(note_id=pk)
        paginator, result_page = utilities.paginate(queryset, request)
        data = NoteVersionSerializer(result_page, many=True)
        return paginator.get_paginated_response(data.data)

    @action(detail=True, methods=["GET"], name="comments")
    def comments(self, request, pk=None):
        """
        This action will be called with the url : /notes/id/comments
        It is responsible for showing all comments of a note
        """

        queryset = Comment.objects.all()
        queryset = queryset.filter(note=pk)
        paginator, result_page = utilities.paginate(queryset, request)
        data = CommentSerializer(result_page, many=True)
        return paginator.get_paginated_response(data.data)


class CommentsViewsets(viewsets.ModelViewSet):
    """
    The viewset for Comment model, it will enable us to Create, update and retrieve
    comments for a particular note, any user with whom the note is shared can comment
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated, UserPermission]
