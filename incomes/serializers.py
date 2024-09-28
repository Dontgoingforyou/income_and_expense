from django.utils import timezone
from rest_framework import serializers

from incomes.models import Income


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'user', 'amount', 'date', 'source', 'category', 'context']
        read_only_fields = ['id', 'user']

    @staticmethod
    def validate_amount(value):
        if value <= 0:
            raise serializers.ValidationError("Сумма должна быть положительным числом")
        return value

    @staticmethod
    def validate_date(value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Нельзя установить дату, которая еще не наступила")
        return value