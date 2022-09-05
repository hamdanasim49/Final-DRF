from rest_framework.response import Response

from ..models import Note
from ..serializers.serializers import (
    NoteSerializer,
)
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets, serializers
from rest_framework import permissions, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
import json
from django.core import serializers
from django.http import HttpResponse
from Note.permissions.permissions import UserPermission
from Note.filters.filters import NotesArchiveFilter
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class NotesViewsets(viewsets.ModelViewSet):
    """
    Viewset for Note model and it is responsible for all the CRUD operations of
    the Note class.
    """

    queryset = Note.objects.all()
    authentication_classes = (JWTAuthentication,)
    serializer_class = NoteSerializer

    pagination_class = PageNumberPagination
    permission_classes = [UserPermission]

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["text"]

    filter_class = NotesArchiveFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(user=user)
        return queryset

    @action(detail=False, methods=["GET"], name="getShared")
    def shared(self, request):
        queryset = Note.objects.all()
        curr_user = request.user
        queryset = queryset.filter(shared_with=curr_user)
        data = serializers.serialize("json", queryset)
        return HttpResponse(data, content_type="application/json")
