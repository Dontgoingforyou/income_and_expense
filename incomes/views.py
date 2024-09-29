from datetime import timedelta
from django.db.models import Sum
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Income
from .serializers import IncomeSerializer

class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IncomeListView(ListView):
    model = Income
    context_object_name = 'incomes'

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)


class IncomeDetailView(DetailView):
    model = Income

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)


class IncomeCreateView(CreateView):
    model = Income
    fields = ("date", "amount", "source", "category", "context")
    success_url = reverse_lazy('incomes:incomes_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class IncomeUpdateView(UpdateView):
    model = Income
    fields = ("date", "amount", "source", "category", "context")
    success_url = reverse_lazy('incomes:incomes_list')

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class IncomeDeleteView(DeleteView):
    model = Income
    success_url = reverse_lazy('incomes:incomes_list')

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)


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