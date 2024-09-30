from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .apps import ExpensesConfig
from .views import ExpenseViewSet, ExpenseListView, ExpenseCreateView, ExpenseDetailView, \
    ExpenseUpdateView, ExpenseDeleteView

app_name = ExpensesConfig.name

router = DefaultRouter()
router.register(r'api', ExpenseViewSet, basename='expense')

urlpatterns = [
    path('', include(router.urls)),
    path('expenses/', ExpenseListView.as_view(), name='expenses_list'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expenses_detail'),
    path('expenses/create/', ExpenseCreateView.as_view(), name='expenses_create'),
    path('expenses/<int:pk>/update/', ExpenseUpdateView.as_view(), name='expenses_update'),
    path('expenses/<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expenses_delete'),
]