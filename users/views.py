from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, TemplateView

from users.forms import CustomUserCreationForm, User


class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:home')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            form.add_error('email', 'Пользователь с таким email уже существует')
            return self.form_invalid(form)

        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return response



class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('users:home')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(View):

    @staticmethod
    def get(request):
        logout(request)
        return redirect('users:login')


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'users/home.html'
    login_url = reverse_lazy('users:login')

