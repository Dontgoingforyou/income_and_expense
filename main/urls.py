from django.urls import path

from .apps import MainConfig
from .views import HomeView, OperationChartDataView

app_name = MainConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('api/operations/chart/', OperationChartDataView.as_view(), name='operation_chart_data'),
]
