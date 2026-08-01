from django.contrib import admin
from .models import WithdrawalRequest

@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'amount', 'rip', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('vendor__email', 'rip')