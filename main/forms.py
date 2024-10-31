from django import forms


class ReportFilterForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Начальная дата',
        required=False
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Конечная дата',
        required=False
    )
    categories = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите категории через запятую'}),
        label='Категории',
        required=False
    )