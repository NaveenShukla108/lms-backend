from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField()
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "full_name", "username", "email", "role", "password", "confirm_password"
        ]
        read_only_fields = ["is_verified", "active_status"]