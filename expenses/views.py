import io
import pandas as pd
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from openpyxl import Workbook
from openpyxl.chart import PieChart, Reference
from rest_framework import permissions
from main.views import BaseDetailView, BaseCreateView, BaseUpdateView, BaseDeleteView, \
    BaseOperationViewSet, BaseOperationListView
from .forms import ExpenseForm
from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseViewSet(BaseOperationViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExpenseListView(BaseOperationListView):
    model = Expense
    template_name = 'main/operation_list.html'

    detail_url_name = 'expenses:expenses_detail'
    update_url_name = 'expenses:expenses_update'
    delete_url_name = 'expenses:expenses_delete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation_type'] = 'Расход'
        return context

    def get_list_url(self):
        return reverse('expenses:expenses_list')

    def get_create_url(self):
        return reverse('expenses:expenses_create')

class ExpenseDetailView(BaseDetailView):
    model = Expense
    template_name = 'main/operation_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = reverse('expenses:expenses_update', kwargs={'pk':self.object.pk})
        context['delete_url'] = reverse('expenses:expenses_delete', kwargs={'pk':self.object.pk})
        context['operation_list_url'] = reverse('expenses:expenses_list')
        return context

class ExpenseCreateView(BaseCreateView):
    model = Expense
    template_name = 'main/operation_form.html'
    success_url = reverse_lazy('expenses:expenses_list')
    form_class = ExpenseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation_type'] = "Расход"
        return context


class ExpenseUpdateView(BaseUpdateView):
    model = Expense
    template_name = 'main/operation_form.html'
    success_url = reverse_lazy('expenses:expenses_list')
    form_class = ExpenseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation_type'] = "Расход"
        return context

class ExpenseDeleteView(BaseDeleteView):
    model = Expense
    template_name = 'main/operation_confirm_delete.html'
    success_url = reverse_lazy('expenses:expenses_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_url'] = reverse('expenses:expenses_detail', kwargs={'pk': self.object.pk})
        return context


def export_expenses_csv(request):
    expenses = Expense.objects.filter(user=request.user).values()
    df = pd.DataFrame(expenses)
    df.drop(columns=['id', 'user_id'], inplace=True)
    df.rename(columns={
        'amount': 'Сумма',
        'date': 'Дата',
        'source': 'Источник',
        'category': 'Категория',
        'context': 'Комментарий'
    }, inplace=True)

    # Подсчет общей суммы доходов
    total_expense = df['Сумма'].sum()
    total_row = pd.DataFrame({'Сумма': [total_expense]})
    df = pd.concat([df, total_row], ignore_index=True)

    # Используем StringIO для создания буфера
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)

    response = HttpResponse(buffer.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'
    return response

def export_expenses_excel(request):
    expenses = Expense.objects.filter(user=request.user).values()
    wb = Workbook()

    # Основной лист с данными
    ws_data = wb.active
    ws_data.title = "Расходы"
    ws_data.append(["Сумма", "Дата", "Источник", "Категория", "Комментарий"])

    for expense in expenses:
        ws_data.append([expense['amount'], expense['date'], expense['source'], expense['category'], expense['context']])

    # Лист с аналитикой
    ws_summary = wb.create_sheet(title='Аналитика')
    total_expense = sum([expense['amount'] for expense in expenses])
    ws_summary.append(['Общая сумма доходов:', total_expense])

    # Диаграмма по категориям
    categories = {}
    for expense in expenses:
        categories[expense['category']] = categories.get(expense['category'], 0) + expense['amount']

    ws_summary.append(['Категория', 'Сумма'])
    for category, amount in categories.items():
        ws_summary.append([category, amount])

    pie = PieChart()
    labels = Reference(ws_summary, min_col=1, min_row=2, max_row=1 + len(categories))
    data = Reference(ws_summary, min_col=2, min_row=2, max_row=1 + len(categories))
    pie.add_data(data, titles_from_data=True)
    pie.set_categories(labels)
    pie.title = 'Расходы по категориям'

    ws_summary.add_chart(pie, 'D5')  # Позиция диаграммы

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="expenses.xlsx"'
    wb.save(response)
    return response