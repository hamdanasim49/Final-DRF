from django.urls import path, include
from .views.views import RegisterUserAPIView

urlpatterns = [
    path("register", RegisterUserAPIView.as_view(), name="register"),
]
