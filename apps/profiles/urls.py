from django.urls import path

from apps.profiles.views import (
    avatar_upload_api_view,
    ProfileDetailAPIView,
    ProfileUpdateAPIView,
)

urlpatterns = [
    path("me/", ProfileDetailAPIView.as_view(), name="profile-me"),
    path("update/", ProfileUpdateAPIView.as_view(), name="profile-update"),
    path("avatar/", avatar_upload_api_view, name="avatar-upload"),
]
