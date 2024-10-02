from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'date', 'source', 'category', 'context']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].label = "Сумма расхода"
        self.fields['source'].label = "Место трат(например: магазин продуктов, аптека и т.п."
        self.fields['category'].label = "Категория расходов(например: продукты, лекарства и т.п."