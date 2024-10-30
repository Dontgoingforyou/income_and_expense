from django.db.models import Sum
from django.utils import timezone
from rest_framework import viewsets, permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from expenses.models import Expense
from incomes.models import Income
from main.mixins import UserQuerySetMixin
from main.models import BaseOperation
from main.serializers import BaseOperationSerializer


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'main/home.html'
    login_url = reverse_lazy('users:login')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Последние операции
        latest_incomes = Income.objects.filter(user=self.request.user).order_by('-date')[:4]
        latest_expenses = Expense.objects.filter(user=self.request.user).order_by('-date')[:4]

        latest_operations = sorted(
            [{'operation': income, 'type': 'Доход'} for income in latest_incomes] +
            [{'operation': expense, 'type': 'Расход' } for expense in latest_expenses],
            key=lambda x: x['operation'].date, reverse=True,
        )

        # Общие доходы и расходы
        total_incomes = Income.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0

        # Аналитика
        balance_change = total_incomes - total_expenses
        saved_percentage = (balance_change / total_incomes * 100) if total_incomes > 0 else "Нет доходов"
        income_expense_ratio = (total_incomes / total_expenses) if total_expenses > 0 else "Нет расходов"

        context.update({
            'total_incomes': total_incomes,
            'total_expenses': total_expenses,
            'balance_change': balance_change,
            'saved_percentage': round(saved_percentage, 2),
            'income_expense_ratio': round(income_expense_ratio, 1),
        })

        context['latest_operations'] = latest_operations
        return context



class BaseOperationViewSet(viewsets.ModelViewSet):
    serializer_class = BaseOperationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BaseOperationListView(LoginRequiredMixin, UserQuerySetMixin, ListView):
    model = BaseOperation
    context_object_name = 'operations'

    detail_url_name = None
    update_url_name = None
    delete_url_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation_list_url'] = self.get_list_url()
        context['operation_create_url'] = self.get_create_url()
        context['operations'] = [
            {
                'operation': operation,
                'detail_url': self.get_detail_url(operation.pk),
                'update_url': self.get_update_url(operation.pk),
                'delete_url': self.get_delete_url(operation.pk),
            }
            for operation in self.get_queryset()
        ]
        return context

    def get_list_url(self):
        raise NotImplementedError

    def get_create_url(self):
        raise NotImplementedError

    def get_detail_url(self, pk):
        return reverse(self.detail_url_name, kwargs={'pk': pk})

    def get_update_url(self, pk):
        return reverse(self.update_url_name, kwargs={'pk': pk})

    def get_delete_url(self, pk):
        return reverse(self.delete_url_name, kwargs={'pk': pk})


class BaseDetailView(LoginRequiredMixin, UserQuerySetMixin, DetailView):
    model = BaseOperation

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class BaseCreateView(LoginRequiredMixin, UserQuerySetMixin, CreateView):
    model = BaseOperation

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BaseUpdateView(LoginRequiredMixin, UserQuerySetMixin, UpdateView):
    model = BaseOperation
    success_url = reverse_lazy('incomes:incomes_list')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class BaseDeleteView(LoginRequiredMixin, UserQuerySetMixin, DeleteView):
    model = BaseOperation
    success_url = reverse_lazy('incomes:incomes_list')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class OperationChartDataView(APIView):
    permission_classes = [IsAuthenticated]  # для доступа пользователь должен быть аутентифицирован

    def get(self, request):
        period = int(request.GET.get('period', '7'))
        today = timezone.now().date()
        if period == 30:
            start_date = today - timezone.timedelta(days=30)
        elif period == 365:
            start_date = today - timezone.timedelta(days=365)
        else:
            start_date = today - timezone.timedelta(days=7)

        # Фильтрация доходов и расходов по диапазону дат
        incomes = Income.objects.filter(user=request.user, date__gte=start_date, date__lte=today)
        expenses = Expense.objects.filter(user=request.user, date__gte=start_date, date__lte=today)

        # Логика для агрегации доходов
        aggregated_income_data = incomes.values('date').annotate(total=Sum('amount')).order_by('date')
        income_data_dict = {item['date']: float(item['total']) for item in aggregated_income_data}

        # Логика для агрегации расходов
        aggregated_expense_data = expenses.values('date').annotate(total=Sum('amount')).order_by('date')
        expense_data_dict = {item['date']: float(item['total']) for item in aggregated_expense_data}

        # Создаем список дат, включая сегодняшнюю
        dates = [start_date + timezone.timedelta(days=i) for i in range(period)]
        labels = [date.strftime('%d.%m.%Y') for date in dates]

        # Получение данных для графика, включая нулевые значения для отсутствующих дат
        income_data = [income_data_dict.get(date, 0) for date in dates]
        expense_data = [expense_data_dict.get(date, 0) for date in dates]

        return Response({'labels': labels, 'incomeData': income_data, 'expenseData': expense_data})

