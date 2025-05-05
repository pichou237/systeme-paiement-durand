from .models import User, OneTimePasscode
from rest_framework import serializers
from django.contrib.auth import authenticate, login
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import send_normal_email
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    password_confirm = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name','phone_number', 'password', 'password_confirm']

    def validate(self, attrs):
        password = attrs.get('password', '')
        password_confirm = attrs.get('password_confirm', '')

        if password != password_confirm:
            raise serializers.ValidationError("passwords do not match !")
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user
    
class VerifyEmailSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=8)

    class Meta:
        model = OneTimePasscode
        fields = ['code']

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=68, write_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    uidb64 = serializers.CharField(max_length=255, read_only=True)
    pk = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['pk', 'email', 'password', 'access_token', 'refresh_token', 'uidb64']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        print(f"{email} - {password}")
        user = authenticate(request, email=email, password=password)
        print(request)
        print(user)

        try:
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        except:
            uidb64 = None
            
        if not user:
            raise AuthenticationFailed("invalid credentials, try again")
        
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")

        user_tokens = user.tokens()
        login(request, user)

        return {
            'email' : user.email, 
            'full_name' : user.get_full_name,
            'uidb64' : uidb64,
            'access_token' : str(user_tokens.get('access')),
            'refresh_token' : str(user_tokens.get('refresh')),
        }