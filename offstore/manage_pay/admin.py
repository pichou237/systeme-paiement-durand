from django.contrib import admin

from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'payment_method', 'currency', 'status', 'date_time', 'transaction_id']
    list_filter = ['payment_method', 'currency', 'status', 'date_time']
    search_fields = ['user__email', 'transaction_id']
    ordering = ['-date_time']
