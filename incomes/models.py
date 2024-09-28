from django.db import models

from users.forms import User

NULLABLE = {'blank': True, 'null': True}

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма дохода", help_text="Введите ваш доход")
    date = models.DateField(verbose_name="Дата получения дохода")
    source = models.CharField(max_length=100, verbose_name="Источник дохода(например зарплата и т.п.)")
    category = models.CharField(max_length=100, verbose_name="Категория дохода(например основной или дополнительных доход)")
    context = models.TextField(**NULLABLE, verbose_name="Комментарий")
