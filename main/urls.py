from django.urls import path
from rest_framework.routers import DefaultRouter

from .apps import MainConfig
from .views import HomeView, OperationChartDataView, BaseOperationViewSet

app_name = MainConfig.name

router = DefaultRouter()
router.register(r'api', BaseOperationViewSet, basename='home')

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('api/operations/chart/', OperationChartDataView.as_view(), name='operation_chart_data'),
] + router.urls
