from django.urls import reverse_lazy, reverse
from rest_framework import permissions
from main.views import BaseDetailView, BaseCreateView, BaseUpdateView, BaseDeleteView, \
    BaseOperationViewSet, BaseOperationListView
from .forms import IncomeForm
from .models import Income
from .serializers import IncomeSerializer


class IncomeViewSet(BaseOperationViewSet):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]


class IncomeListView(BaseOperationListView):
    model = Income
    template_name = 'main/operation_list.html'

    detail_url_name = 'incomes:incomes_detail'
    update_url_name = 'incomes:incomes_update'
    delete_url_name = 'incomes:incomes_delete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation_type'] = 'Доход'
        return context

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
    form_class = IncomeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation_type'] = "Доход"
        return context


class IncomeUpdateView(BaseUpdateView):
    model = Income
    template_name = 'main/operation_form.html'
    success_url = reverse_lazy('incomes:incomes_list')
    form_class = IncomeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation_type'] = "Доход"
        return context

class IncomeDeleteView(BaseDeleteView):
    model = Income
    template_name = 'main/operation_confirm_delete.html'
    success_url = reverse_lazy('incomes:incomes_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_url'] = reverse('incomes:incomes_detail', kwargs={'pk': self.object.pk})
        return context
