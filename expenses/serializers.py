from expenses.models import Expense
from main.serializers import BaseOperationSerializer


class ExpenseSerializer(BaseOperationSerializer):
    class Meta(BaseOperationSerializer.Meta):
        model = Expense