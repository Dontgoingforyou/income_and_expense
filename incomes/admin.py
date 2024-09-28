from django.contrib import admin

from incomes.models import Income


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'date', 'source', 'category')
    list_filter = ('user', 'date', 'category')
    search_fields = ('source', 'category', 'comment')