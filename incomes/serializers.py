from incomes.models import Income
from main.serializers import BaseOperationSerializer


class IncomeSerializer(BaseOperationSerializer):
    class Meta(BaseOperationSerializer.Meta):
        model = Income