from rest_framework import viewsets, permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView

from main.mixins import UserQuerySetMixin
from main.models import BaseOperation


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'main/home.html'
    login_url = reverse_lazy('users:login')


class BaseOperationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BaseOperationListView(LoginRequiredMixin, UserQuerySetMixin, ListView):
    model = BaseOperation
    context_object_name = 'operations'

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
        return reverse('incomes:incomes_detail', kwargs={'pk': pk})

    def get_update_url(self, pk):
        return reverse('incomes:incomes_update', kwargs={'pk': pk})

    def get_delete_url(self, pk):
        return reverse('incomes:incomes_delete', kwargs={'pk': pk})


class BaseDetailView(LoginRequiredMixin, UserQuerySetMixin, DetailView):
    model = BaseOperation

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class BaseCreateView(LoginRequiredMixin, UserQuerySetMixin, CreateView):
    model = BaseOperation
    fields = ("date", "amount", "source", "category", "context")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BaseUpdateView(LoginRequiredMixin, UserQuerySetMixin, UpdateView):
    model = BaseOperation
    fields = ("date", "amount", "source", "category", "context")
    success_url = reverse_lazy('incomes:incomes_list')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class BaseDeleteView(LoginRequiredMixin, UserQuerySetMixin, DeleteView):
    model = BaseOperation
    success_url = reverse_lazy('incomes:incomes_list')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
