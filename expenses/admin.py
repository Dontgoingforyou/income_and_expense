from django.contrib import admin

from expenses.models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'date', 'source', 'category')
    list_filter = ('user', 'date', 'category')
    search_fields = ('source', 'category', 'comment')