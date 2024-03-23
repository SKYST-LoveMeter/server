from .models import User
from rest_framework import serializers

class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "real_name",
            "password"
        )

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "password"
        )
