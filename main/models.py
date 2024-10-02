from django.conf import settings
from django.db import models


NULLABLE = {'blank': True, 'null': True}

class BaseOperation(models.Model):
    OPERATION_TYPES = (
        ('income', 'Доход'),
        ('expense', 'Расход'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_operations')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма", help_text="Введите сумму")
    date = models.DateField(verbose_name="Дата")
    source = models.CharField(max_length=100, verbose_name="Источник")
    category = models.CharField(max_length=100, verbose_name="Категория")
    context = models.TextField(**NULLABLE, verbose_name="Комментарий")

    class Meta:
        abstract = True
        ordering = ['-date']

    def operation_type(self):
        pass