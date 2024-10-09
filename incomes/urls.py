from django.urls import path
from rest_framework.routers import DefaultRouter
from .apps import IncomesConfig
from .views import IncomeViewSet, IncomeListView, IncomeCreateView, IncomeDetailView, \
    IncomeUpdateView, IncomeDeleteView, export_incomes_csv, export_incomes_excel

app_name = IncomesConfig.name

router = DefaultRouter()
router.register(r'api/incomes', IncomeViewSet, basename='income')

urlpatterns = [
    path('', IncomeListView.as_view(), name='incomes_list'),
    path('incomes/<int:pk>/', IncomeDetailView.as_view(), name='incomes_detail'),
    path('incomes/create/', IncomeCreateView.as_view(), name='incomes_create'),
    path('incomes/<int:pk>/update/', IncomeUpdateView.as_view(), name='incomes_update'),
    path('incomes/<int:pk>/delete/', IncomeDeleteView.as_view(), name='incomes_delete'),
    path('export/csv/', export_incomes_csv, name='export_incomes_csv'),
    path('export/excel/', export_incomes_excel, name='export_incomes_excel'),
] + router.urls
