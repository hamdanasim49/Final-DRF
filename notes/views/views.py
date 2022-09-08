from rest_framework.response import Response

from ..models import Note, NoteVersion, Comment
from ..serializers.serializers import (
    NoteSerializer,
    NoteVersionSerializer,
    CommentSerializer,
    ObjectNoteSerializer,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets, serializers
from rest_framework import permissions, filters, mixins
from rest_framework.pagination import PageNumberPagination
from notes.permissions.permissions import UserPermission
from notes.filters.filters import NotesArchiveFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action


class NotesViewsets(viewsets.ModelViewSet):
    """
    Viewset for notes model and it is responsible for all the CRUD operations of
    the notes class.
    """

    queryset = Note.objects.all()
    authentication_classes = (JWTAuthentication,)
    serializer_class = NoteSerializer

    pagination_class = PageNumberPagination
    permission_classes = [UserPermission]

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["text"]

    filter_class = NotesArchiveFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ObjectNoteSerializer
        return NoteSerializer

    """
    #TODO: We will move this functionality into filters
    """

    def get_queryset(self):
        user = self.request.user
        if self.request.GET.get("shared") == "true":
            queryset = Note.objects.all()
            if self.request.GET.get("archive") == "true":
                queryset = queryset.filter(shared_with=user).filter(archive=True)
                return queryset
            elif self.request.GET.get("archive") == "false":
                queryset = queryset.filter(shared_with=user).filter(archive=False)
                return queryset
            else:
                queryset = queryset.filter(shared_with=user)
                return queryset

        elif self.request.GET.get("archive") == "true":
            queryset = self.queryset.filter(user=user).filter(archive=True)
            return queryset
        elif self.request.GET.get("archive") == "false":
            queryset = self.queryset.filter(user=user).filter(archive=False)
            return queryset
        else:
            queryset = self.queryset.filter(user=user)
            queryset1 = self.queryset.filter(shared_with=user)
            new_queryset = (queryset | queryset1).distinct()
            return new_queryset

    """
    This action will be called with the url : /notes/id/versions
    It is responsible for showing all the versions of a note
    """

    @action(detail=True, methods=["GET"], name="versions")
    def versions(self, request, pk=None):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        queryset = NoteVersion.objects.all()
        queryset = queryset.filter(note_id=pk)
        result_page = paginator.paginate_queryset(queryset, request)
        data = NoteVersionSerializer(result_page, many=True)
        return paginator.get_paginated_response(data.data)

    """
        This action will be called with the url : /notes/id/comments
        It is responsible for showing all comments of a note
    """

    @action(detail=True, methods=["GET"], name="comments")
    def comments(self, request, pk=None):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        queryset = Comment.objects.all()
        queryset = queryset.filter(note=pk)
        result_page = paginator.paginate_queryset(queryset, request)
        data = CommentSerializer(result_page, many=True)
        return paginator.get_paginated_response(data.data)


class CommentsViewsets(viewsets.ModelViewSet):
    """
    The viewset for Comment model, it will enable us to Create, update and retrieve
    comments for a particular note, any user with whom the note is shared can comment
    """

    queryset = Comment.objects.all()
    authentication_classes = (JWTAuthentication,)
    serializer_class = CommentSerializer

    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated, UserPermission]
