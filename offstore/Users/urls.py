from django.urls import path
from .views import (
    PasswordResetRequestView,
    SetNewPasswordView,
    UpdateProfileView,
    UserRegisterView,
    VerifyEmailView,
    LoginUserView,
    PasswordResetConfirmView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
    path('update-profile/<int:pk>/', UpdateProfileView.as_view(), name='update-profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),]
