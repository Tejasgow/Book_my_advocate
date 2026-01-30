from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum

from .models import Payment, Refund
from .services import razorpay_client
from .utils import generate_invoice
from app.appointments.models import Appointment
from django.conf import settings

class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        appointment = Appointment.objects.get(id=request.data['appointment_id'])

        amount = int(appointment.fee * 100)

        order = razorpay_client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })

        Payment.objects.create(
            appointment=appointment,
            client=appointment.client,
            amount=appointment.fee,
            razorpay_order_id=order['id']
        )

        return Response({
            "order_id": order['id'],
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "amount": amount
        })


class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        payment = Payment.objects.get(
            razorpay_order_id=data['razorpay_order_id']
        )

        razorpay_client.utility.verify_payment_signature(data)

        payment.razorpay_payment_id = data['razorpay_payment_id']
        payment.razorpay_signature = data['razorpay_signature']
        payment.status = 'SUCCESS'
        payment.save()

        payment.appointment.is_paid = True
        payment.appointment.save()

        return Response({"message": "Payment successful"})


class PaymentStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({
            "total_payments": Payment.objects.count(),
            "successful_payments": Payment.objects.filter(status='SUCCESS').count(),
            "total_revenue": Payment.objects.filter(
                status='SUCCESS'
            ).aggregate(Sum('amount'))['amount__sum'] or 0,
            "refunds": Refund.objects.count()
        })

class InvoiceDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, payment_id):
        payment = Payment.objects.get(id=payment_id)
        return generate_invoice(payment)

class RefundPaymentView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        payment_id = request.data.get('payment_id')
        reason = request.data.get('reason', 'No reason provided')

        payment = Payment.objects.get(id=payment_id)

        if payment.status != 'SUCCESS':
            return Response({"error": "Only successful payments can be refunded."}, status=400)

        refund_amount = int(payment.amount * 100)

        refund = razorpay_client.payment.refund(payment.razorpay_payment_id, {
            "amount": refund_amount,
            "speed": "normal",
            "notes": {"reason": reason}
        })

        Refund.objects.create(
            payment=payment,
            amount=payment.amount,
            reason=reason,
            razorpay_refund_id=refund['id'],
            status='INITIATED'
        )

        payment.status = 'REFUNDED'
        payment.save()

        return Response({"message": "Refund initiated successfully."})
    