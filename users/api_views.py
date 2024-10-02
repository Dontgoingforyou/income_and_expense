from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken



class RegisterAPIView(generics.CreateAPIView):
    """ Класс позволяет регистрировать новых пользователей через API.
        После создания автоматически создается токен и возвращается с данными пользователя """

    User = get_user_model()

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class CustomObtainAuthToken(ObtainAuthToken):
    """ Класс расширяет стандартный DRF ObtainAuthToken для возврата доп данных о
        пользователе при получении токена """

    User = get_user_model()

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'user_id': token.user_id,
            'username': token.user.username
        })