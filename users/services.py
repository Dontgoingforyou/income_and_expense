from django.conf import settings
from django.core.mail import send_mail

from .models import CustomUser

def send_registration_email(custom_user: CustomUser):
    send_mail(
        'Благодарю за регистрацию!',
        f'{custom_user.username}! Спасибо за то, что решили воспользоваться данным приложением!',
        settings.EMAIL_HOST_USER,
        [custom_user.email]
    )