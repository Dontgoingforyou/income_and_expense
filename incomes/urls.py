from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .apps import IncomesConfig
from .views import IncomeViewSet, IncomeListView, IncomeCreateView, IncomeChartDataView

app_name = IncomesConfig.name

router = DefaultRouter()
router.register(r'income-list', IncomeViewSet, basename='income')

urlpatterns = [
    path('', include(router.urls)),
    path('incomes_list/', IncomeListView.as_view(), name='incomes_list'),
    path('incomes_create/', IncomeCreateView.as_view(), name='incomes_create'),
    path('incomes-chart-data/', IncomeChartDataView.as_view(), name='incomes_chart_data'),
]