from django.urls import path
from .api_views import RegisterAPIView, CustomObtainAuthToken

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='api_register'),
    path('login/', CustomObtainAuthToken.as_view(), name='api_login'),
]