from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response

from apps.profiles.models import Profile
from apps.profiles.serializers import (
    AvatarUploadSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
)

from .tasks import upload_avatar_to_cloudinary

User = get_user_model()


class ProfileDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self) -> Profile:
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            raise NotFound("Profile not found")


class ProfileUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdateProfileSerializer

    def get_object(self) -> Profile:
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def perform_update(self, serializer: UpdateProfileSerializer) -> Profile:
        user_data = serializer.validated_data.pop("user", {})
        if (
                "username" in user_data
                and User.objects.filter(username=user_data["username"]).exists()
        ):
            raise PermissionDenied("This username is already taken")
        profile = serializer.save()
        User.objects.filter(id=self.request.user.id).update(**user_data)
        return profile


@api_view(["PATCH"])
@permission_classes([permissions.IsAuthenticated])
def avatar_upload_api_view(request):
    profile = request.user.profile
    serializer = AvatarUploadSerializer(profile, data=request.data)

    if serializer.is_valid():
        image = serializer.validated_data["avatar"]

        image_content = image.read()

        upload_avatar_to_cloudinary.delay(str(profile.id), image_content)

        return Response(
            {"message": "Avatar upload started."}, status=status.HTTP_202_ACCEPTED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
