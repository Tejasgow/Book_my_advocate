from rest_framework import serializers
from .models import Payment, Refund

# ----------------------------------------------
# Payment Serializer
# ----------------------------------------------

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['razorpay_order_id','razorpay_payment_id',
                            'razorpay_signature','status']
        
# ----------------------------------------------
# Refund Serializer
# ----------------------------------------------
class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = '__all__'
        read_only_fields = ['refund_id','created_at']
