from .models import User, OneTimePasscode
from .serializers import (
    UserRegisterSerializer, VerifyEmailSerializer, UserLoginSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer, SetNewPasswordSerializer
)
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.generics import GenericAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .utils import send_code_to_user
from .permissions import IsManager, IsUser
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import logging

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class UserRegisterView(GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Construire les données pour l'email
        email_data = {
            'email_subject': 'Welcome to our platform!',
            'email_body': f"Hi {user.first_name},\n\nThank you for registering on our platform.",
            'to_email': user.email
        }

        otp_sent = send_code_to_user(email_data)
        if not otp_sent:
            logger.error(f"Échec de l'envoi de l'OTP pour {user.email}")
            return Response({"error": "Échec de l'envoi de l'e-mail."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "data": serializer.data,
            "message": f"Utilisateur {user.first_name} créé avec succès. Un code OTP a été envoyé à votre email.",
        }, status=status.HTTP_201_CREATED)
@method_decorator(csrf_exempt, name='dispatch')
class VerifyEmailView(GenericAPIView):
    serializer_class = VerifyEmailSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get("code")
        try:
            otp = OneTimePasscode.objects.get(code=code)
            user = otp.user

            if user.is_verified:
                return Response({"message": "Utilisateur déjà vérifié."}, status=status.HTTP_200_OK)

            user.is_verified = True
            user.save()
            return Response({"message": "Email vérifié avec succès."}, status=status.HTTP_200_OK)

        except OneTimePasscode.DoesNotExist:
            return Response({"message": "Code OTP invalide."}, status=status.HTTP_404_NOT_FOUND)

@method_decorator(csrf_exempt, name='dispatch')
class LoginUserView(GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [IsUser, IsManager]

@method_decorator(csrf_exempt, name='dispatch')
class UpdateProfileView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [IsUser]

@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response({"message": "OTP envoyé avec succès."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({
                "message": "OTP vérifié avec succès.",
                "uidb64": serializer.validated_data['uidb64'],
                "token": serializer.validated_data['token']
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class SetNewPasswordView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SetNewPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
