from django.urls import path
from .views import PasswordResetConfirm, PasswordResetRequestView, SetNewPasswordView, UpdateProfileView, UserRegisterView, VerifyEmailView, LogoutUserView, LoginUserView, RefreshTokenView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password-reset-confirm'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
    path('update-profile/<int:pk>/', UpdateProfileView.as_view(), name='update-profile'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh_token'),
   
    
]