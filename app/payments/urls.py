from django.urls import path
from .views import (
    CreatePaymentView,
    VerifyPaymentView,
    RefundPaymentView,
    PaymentStatsView,
    InvoiceDownloadView
)

urlpatterns = [
    path('payments/create/', CreatePaymentView.as_view()),
    path('payments/verify/', VerifyPaymentView.as_view()),
    path('payments/refund/', RefundPaymentView.as_view()),
    path('payments/stats/', PaymentStatsView.as_view()),
    path('payments/<int:payment_id>/invoice/', InvoiceDownloadView.as_view()),
]
