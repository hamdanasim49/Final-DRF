from django.urls import path, include
from notes.views.views import NotesViewsets, CommentsViewsets
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"notes", NotesViewsets)
router.register(r"comments", CommentsViewsets)

urlpatterns = [
    path("", include(router.urls)),
]
