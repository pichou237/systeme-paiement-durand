from .views import UserRegisterView
from django.urls import path, include




urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
]