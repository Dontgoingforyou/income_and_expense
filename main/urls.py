from django.urls import path

from .apps import MainConfig
from .views import HomeView

app_name = MainConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]