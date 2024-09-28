from django.urls import path

from users.apps import UsersConfig
from users.views import HomeView, RegisterView, LoginView, LogoutView

app_name = UsersConfig.name

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
