# payments/dashboard.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Sum, Count, Q
from decimal import Decimal

from .models import Payment, Refund


class PaymentDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # =================================================
        # ADVOCATE PAYMENT DASHBOARD
        # =================================================
        if user.role == "ADVOCATE":
            if not hasattr(user, "advocate_profile"):
                return Response(
                    {"error": "Advocate profile not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            advocate = user.advocate_profile
            
            # Get payments from appointments with this advocate
            payments = Payment.objects.filter(
                appointment__advocate=advocate
            )

            total_revenue = payments.filter(
                status='SUCCESS'
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

            stats = {
                "total_transactions": payments.count(),
                "successful_payments": payments.filter(status='SUCCESS').count(),
                "failed_payments": payments.filter(status='FAILED').count(),
                "pending_payments": payments.filter(status='CREATED').count(),
                "total_revenue": str(total_revenue),
                "average_transaction": str(
                    total_revenue / max(
                        payments.filter(status='SUCCESS').count(), 1
                    ) if payments.filter(status='SUCCESS').count() > 0 else Decimal('0.00')
                ),
            }

            # Recent transactions
            recent_payments = payments.order_by('-created_at')[:5]
            recent_data = [
                {
                    "id": payment.id,
                    "client": payment.client.user.first_name,
                    "amount": str(payment.amount),
                    "status": payment.status,
                    "date": payment.created_at,
                }
                for payment in recent_payments
            ]

            return Response({
                "role": "ADVOCATE",
                "stats": stats,
                "recent_transactions": recent_data
            }, status=status.HTTP_200_OK)

        # =================================================
        # CLIENT PAYMENT DASHBOARD
        # =================================================
        elif user.role == "CLIENT":
            if not hasattr(user, "client_profile"):
                return Response(
                    {"error": "Client profile not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            client = user.client_profile
            
            payments = Payment.objects.filter(client=client)

            total_spent = payments.filter(
                status='SUCCESS'
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

            stats = {
                "total_transactions": payments.count(),
                "successful_payments": payments.filter(status='SUCCESS').count(),
                "failed_payments": payments.filter(status='FAILED').count(),
                "pending_payments": payments.filter(status='CREATED').count(),
                "total_spent": str(total_spent),
                "refunds_issued": Refund.objects.filter(
                    payment__client=client
                ).count(),
            }

            # Recent transactions
            recent_payments = payments.order_by('-created_at')[:5]
            recent_data = [
                {
                    "id": payment.id,
                    "advocate": payment.appointment.advocate.user.first_name,
                    "amount": str(payment.amount),
                    "status": payment.status,
                    "date": payment.created_at,
                }
                for payment in recent_payments
            ]

            return Response({
                "role": "CLIENT",
                "stats": stats,
                "recent_transactions": recent_data
            }, status=status.HTTP_200_OK)

        # =================================================
        # ADMIN PAYMENT DASHBOARD
        # =================================================
        elif user.role == "ADMIN":
            payments = Payment.objects.all()
            refunds = Refund.objects.all()

            total_revenue = payments.filter(
                status='SUCCESS'
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

            total_refunded = refunds.aggregate(
                total=Sum('amount')
            )['total'] or Decimal('0.00')

            stats = {
                "total_transactions": payments.count(),
                "successful_payments": payments.filter(status='SUCCESS').count(),
                "failed_payments": payments.filter(status='FAILED').count(),
                "pending_payments": payments.filter(status='CREATED').count(),
                "total_revenue": str(total_revenue),
                "total_refunded": str(total_refunded),
                "net_revenue": str(total_revenue - total_refunded),
                "total_refunds": refunds.count(),
                "average_transaction": str(
                    total_revenue / max(
                        payments.filter(status='SUCCESS').count(), 1
                    ) if payments.filter(status='SUCCESS').exists() else Decimal('0.00')
                ),
            }

            return Response({
                "role": "ADMIN",
                "stats": stats
            }, status=status.HTTP_200_OK)

        return Response(
            {"error": "Role not recognized"},
            status=status.HTTP_400_BAD_REQUEST
        )
