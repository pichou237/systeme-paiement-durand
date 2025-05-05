from .views import UserRegisterView, LoginUserView, VerifyEmailView
from django.urls import path, include




urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),



]