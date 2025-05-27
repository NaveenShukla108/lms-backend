from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
import uuid
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import os
from rest_framework_simplejwt.tokens import RefreshToken


login_methods = (
    ("password", "PASSWORD"),
    ("magic link", "MAGIC LINK")
)


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "full_name", "username", "email", "role", "password", "confirm_password"
        ]
        read_only_fields = ["is_verified", "active_status", "username"]

    
    def validate(self, attrs):  
    
        check_user = User.objects.filter(email=attrs["email"])
        if check_user.exists():
            raise serializers.ValidationError("User already exists")
        
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("password & confirm password do not match")
        
        return attrs

    def create(self, validated_data):    
        validated_data.pop("confirm_password")
        validated_data["username"] = uuid.uuid4()
    
        user = User.objects.create_user(
            username=validated_data["username"],
            full_name=validated_data["full_name"],
            email=validated_data["email"],
            role=validated_data["role"],
            password=validated_data["password"]  # The password is hashed automatically
        )
        user.save()

        return user
    

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)
    login_with = serializers.ChoiceField(choices=login_methods, required=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['email', 'login_with', 'password']

    def validate(self, attrs):
        
        if attrs['login_with'] == 'password':
            
            if 'password' not in attrs:
                raise serializers.ValidationError("password is required when selected 'password' in the dropdown")
            
            try:
                user = User.objects.get(email=attrs.get('email'))
            except User.DoesNotExist:
                raise serializers.ValidationError("User does not exists")
            
            if not user.check_password(attrs.get('password')):
                raise serializers.ValidationError("Incorrect Password")
            
            refresh_token = RefreshToken.for_user(user)
            attrs['refresh_token'] = str(refresh_token)
            attrs['access_token'] = str(refresh_token.access_token)
        
            attrs['user'] = user

        elif attrs['login_with'] == 'magic link':
            magic_serializer = MagicLinkRequestSerializer(data={'email':attrs['email']})
            magic_serializer.is_valid(raise_exception=True)
            magic_serializer.save()
            attrs['message'] = "Magic link has been sent to your email."

        return attrs
    

class MagicLinkRequestSerializer(serializers.ModelSerializer):
    
    token = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'token']

    def validate(self, attrs):
        
        email = attrs.get('email')
        token = attrs.get('token')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User Not Found !")
        
        self.user = user

        if token:
        
            if user.magic_login_token != token:
                raise serializers.ValidationError("Invalid Token")
            if not user.magic_login_token_expiry or user.magic_login_token_expiry < timezone.now():
                raise serializers.ValidationError("Token Expired")
            
        return attrs
    
    def create(self, validated_data):
        
        user = self.user
        token = validated_data.get('token')

        if token:
            # Token is valid → clear token & login
            user.magic_login_token = None
            user.magic_login_token_expiry = None
            user.save()

            refresh_token = RefreshToken.for_user(user)
            validated_data['refresh_token'] = str(refresh_token)
            validated_data['access_token'] = str(refresh_token.access_token)

            validated_data.pop('token', None)
            
            return {
                "user": validated_data,
                "message": "Login successful", 
                }
        
        else:
            magic_token = str(uuid.uuid4())
            user.magic_login_token = magic_token
            user.magic_login_token_expiry = timezone.now() + timedelta(minutes=10)
            user.save()

            magic_api_url = reverse('magic-link-verify-list')
            magic_link = f"{os.environ.get('domain')}{magic_api_url}?email={user.email}&token={magic_token}"

            mail_status = send_mail(
                "Your Magic Link is Here !!",
                f"Click to login: {magic_link}",    
                from_email=os.environ.get('from_email'),
                recipient_list=[user.email],
            )
            if mail_status:
                return {"message": "Magic login link sent to your email."}
            
            return {"mail not sent"}
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "role", "full_name"] 