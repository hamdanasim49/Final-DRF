from rest_framework.response import Response

from ..models import Note
from ..serializers.serializers import (
    NoteSerializer,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets, serializers
from rest_framework import permissions, filters
from rest_framework.pagination import PageNumberPagination
from notes.permissions.permissions import UserPermission
from notes.filters.filters import NotesArchiveFilter
from django_filters.rest_framework import DjangoFilterBackend


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

    """
    TODO: We will move this functionality into filters
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
            return queryset
