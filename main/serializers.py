from rest_framework import serializers
from .models import BaseOperation


class BaseOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseOperation
        fields = ['id', 'user', 'amount', 'date', 'source', 'category', 'context']



