from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        """ Метод вызывается при инициализации приложения.
            Импорт signals.py для регистрации сигналов """

        import users.signals
