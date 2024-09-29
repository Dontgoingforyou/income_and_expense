from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .apps import IncomesConfig
from .views import IncomeViewSet, IncomeListView, IncomeCreateView, IncomeChartDataView, IncomeDetailView, \
    IncomeUpdateView, IncomeDeleteView

app_name = IncomesConfig.name

router = DefaultRouter()
router.register(r'api', IncomeViewSet, basename='income')

urlpatterns = [
    path('', include(router.urls)),
    path('incomes/', IncomeListView.as_view(), name='incomes_list'),
    path('incomes/<int:pk>/', IncomeDetailView.as_view(), name='incomes_detail'),
    path('incomes/create/', IncomeCreateView.as_view(), name='incomes_create'),
    path('incomes/<int:pk>/update/', IncomeUpdateView.as_view(), name='incomes_update'),
    path('incomes/<int:pk>/delete/', IncomeDeleteView.as_view(), name='incomes_delete'),
    path('incomes-chart-data/', IncomeChartDataView.as_view(), name='incomes_chart_data'),
]
