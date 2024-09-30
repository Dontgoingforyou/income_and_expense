from main.models import BaseOperation


class Expense(BaseOperation):
    def save(self, *args, **kwargs):
        self.operation_type = 'income'
        super().save(*args, **kwargs)
