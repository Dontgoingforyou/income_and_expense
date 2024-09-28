from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from rest_framework import viewsets, permissions
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