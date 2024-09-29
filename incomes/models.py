from main.models import BaseOperation


class Income(BaseOperation):
    def save(self, *args, **kwargs):
        self.operation_type = 'income'
        super().save(*args, **kwargs)