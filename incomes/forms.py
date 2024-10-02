from django import forms
from .models import Income


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'date', 'source', 'category', 'context']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].label = "Сумма дохода"
        self.fields['source'].label = "Источник дохода(например: основная работа, фриланс и т.п.)"
        self.fields['category'].label = "Категория дохода(например: основной, дополнительный и т.п.)"