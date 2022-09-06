from django.urls import path, include
from notes.views.views import NotesViewsets
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"notes", NotesViewsets)

urlpatterns = [
    path("", include(router.urls)),
]
