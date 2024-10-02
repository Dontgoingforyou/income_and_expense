from main.models import BaseOperation


class Expense(BaseOperation):
    class Meta:
        verbose_name = "Расход"
        verbose_name_plural = "Расходы"

    def save(self, *args, **kwargs):
        self.source = 'Расход'
        super().save(*args, **kwargs)

    def operation_type(self):
        return self.OPERATION_TYPES[1][1]
