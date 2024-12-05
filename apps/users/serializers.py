from django.contrib.auth import get_user_model
from django_countries.serializer_fields import CountryField
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    full_name = serializers.ReadOnlyField(source="get_full_name")
    gender = serializers.CharField(source="profile.gender")
    country = CountryField(source="profile.country")
    avatar = serializers.ReadOnlyField(source="profile.avatar.url")

    class Meta(UserSerializer.Meta):
        model = User
        fields = [
            "id",
            "username",
            "full_name",
            "email",
            "gender",
            "country",
            "avatar",
            "date_joined",
        ]


class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "password"]
