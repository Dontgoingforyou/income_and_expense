from main.models import BaseOperation


class Income(BaseOperation):
    class Meta:
        verbose_name = "Доход"
        verbose_name_plural = "Доходы"

    def save(self, *args, **kwargs):
        self.source = 'Доход'
        super().save(*args, **kwargs)

    def operation_type(self):
        return self.OPERATION_TYPES[0][1]