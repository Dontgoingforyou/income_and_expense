from datetime import timedelta
from django.db.models import Sum
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from main.views import BaseDetailView, BaseCreateView, BaseUpdateView, BaseDeleteView, \
    BaseOperationViewSet, BaseOperationListView
from .models import Income
from .serializers import IncomeSerializer


class IncomeViewSet(BaseOperationViewSet):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]


class IncomeListView(BaseOperationListView):
    model = Income
    template_name = 'main/operation_list.html'

    def get_list_url(self):
        return reverse('incomes:incomes_list')

    def get_create_url(self):
        return reverse('incomes:incomes_create')

class IncomeDetailView(BaseDetailView):
    model = Income
    template_name = 'main/operation_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = reverse('incomes:incomes_update', kwargs={'pk':self.object.pk})
        context['delete_url'] = reverse('incomes:incomes_delete', kwargs={'pk':self.object.pk})
        context['operation_list_url'] = reverse('incomes:incomes_list')
        return context

class IncomeCreateView(BaseCreateView):
    model = Income
    template_name = 'main/operation_form.html'
    success_url = reverse_lazy('incomes:incomes_list')


class IncomeUpdateView(BaseUpdateView):
    model = Income
    template_name = 'main/operation_form.html'
    success_url = reverse_lazy('incomes:incomes_list')

class IncomeDeleteView(BaseDeleteView):
    model = Income
    template_name = 'main/operation_confirm_delete.html'
    success_url = reverse_lazy('incomes:incomes_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_url'] = reverse('incomes:incomes_detail', kwargs={'pk': self.object.pk})
        return context


class IncomeChartDataView(APIView):
    permission_classes = [IsAuthenticated]  # для доступа пользователь должен быть аутентифицирован

    def get(self, request):
        period = int(request.GET.get('period', '7'))
        today = timezone.now().date()  # получаю сегодняшнюю дату
        start_date = today - timedelta(days=period - 1)  # с какой даты начинать собирать данные
        incomes = Income.objects.filter(user=request.user, date__gte=start_date, date__lte=today)

        # Агрегация данные по дате, .annotate вычисляет общую сумму для каждой даты
        aggregated_data = incomes.values('date').annotate(total=Sum('amount')).order_by('date')

        # Формирование полного списка дат
        dates = [start_date + timedelta(days=i) for i in range(period)]
        labels = [date.strftime('%d.%m.%Y') for date in dates]
        data = []

        # Заполнение данных, устанока 0 для дат без доходов
        income_dict = {item['date']: float(item['total']) for item in aggregated_data}
        for date in dates:
            total = income_dict.get(date, 0)
            data.append(total)

        # many=True - сериализация нескольких объектов
        serializer = IncomeSerializer(incomes, many=True)

        # labels - метки дат для оси Х графика, data - доходы для соотв. дат, incomes - данные о доходах
        return Response({'labels': labels, 'data': data, 'incomes': serializer.data})