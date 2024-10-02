from django.urls import reverse_lazy, reverse
from rest_framework import permissions
from main.views import BaseDetailView, BaseCreateView, BaseUpdateView, BaseDeleteView, \
    BaseOperationViewSet, BaseOperationListView
from .forms import ExpenseForm
from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseViewSet(BaseOperationViewSet):
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
