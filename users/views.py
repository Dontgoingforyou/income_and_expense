from multiprocessing.managers import Token

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView

from users.forms import User, CustomUserCreationForm
from users.services import send_registration_email


class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            form.add_error('email', 'Пользователь с таким email уже существует')
            return self.form_invalid(form)

        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        send_registration_email(user)

        Token.objects.get_or_create(user=user)

        return response



class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('users:login')




