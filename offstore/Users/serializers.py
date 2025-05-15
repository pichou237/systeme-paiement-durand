from .models import User, OneTimePasscode
from rest_framework import serializers
from django.contrib.auth import authenticate, login
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import send_code_to_user, generateOtp
from rest_framework_simplejwt.tokens import RefreshToken
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    password_confirm = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError("Passwords do not match!")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')  # Retirer le champ non nécessaire
        return User.objects.create_user(**validated_data)


class VerifyEmailSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=8)

    class Meta:
        model = OneTimePasscode
        fields = ['code']


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=68, write_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'access_token', 'refresh_token', 'user_id']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')

        user = authenticate(request, username=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")

        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")

        tokens = user.tokens()
        login(request, user)

        return {
            'email': user.email,
            'full_name': user.get_full_name,  # Utilisation correcte de la propriété
            'access_token': str(tokens.get('access')),
            'refresh_token': str(tokens.get('refresh')),
            'user_id': user.id
        }


class PasswordResetRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("No user found with this email address.")
        code = generateOtp()
        expires_at = timezone.now() + timezone.timedelta(minutes=10)
        OneTimePasscode.objects.update_or_create(
            user=user,
            defaults={'code': code, 'expires_at': expires_at}
        )

        email_body = (
            f"Hi {user.first_name or 'user'},\n\n"
            f"Use this code to reset your password: {code}\n\n"
            "This code will expire in 10 minutes."
        )

        # Envoyer l'email
        send_code_to_user({
            'email_body': email_body,
            'email_subject': 'Your code for password reset',
            'to_email': user.email
        })

        return attrs

class PasswordResetConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        code = attrs.get('code')

        try:
            otp_record = OneTimePasscode.objects.get(code=code)
        except OneTimePasscode.DoesNotExist:
            raise serializers.ValidationError("Invalid code.")

        if otp_record.is_expired():
            raise serializers.ValidationError("Code has expired.")

        user_id = otp_record.user.id
        attrs['uidb64'] = urlsafe_base64_encode(smart_bytes(user_id))
        attrs['token'] = PasswordResetTokenGenerator().make_token(otp_record.user)
        return attrs


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, write_only=True)
    confirm_password = serializers.CharField(min_length=6, write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        uidb64 = attrs.get('uidb64')
        token = attrs.get('token')

        if password != confirm_password:
            raise AuthenticationFailed("Passwords do not match.")

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise AuthenticationFailed("Invalid or expired reset link.")

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise AuthenticationFailed("Token is invalid or has expired.")

        user.set_password(password)
        user.save()

        return {"message": "Password reset successful."}