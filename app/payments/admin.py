from django.contrib import admin
from .models import Payment, Refund


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'appointment', 'client', 'amount', 'status', 'created_at')
    list_filter = ('status',)
    readonly_fields = ('razorpay_order_id', 'razorpay_payment_id')


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('refund_id', 'payment', 'amount', 'created_at')
