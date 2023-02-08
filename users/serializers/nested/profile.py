from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from users.models.profile import Profile

User = get_user_model()


class ProfileShortSerializer(serializers.ModelSerializer): # наследуемы сериализтор профиля

    class Meta:
        model = Profile
        fields = (
            'telegram_id',
        )


class ProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'telegram_id',
        )