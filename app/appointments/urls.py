from django.urls import path
from .views import (
    AppointmentCreateView,
    UserAppointmentListView,
    AdvocateAppointmentListView,
    AppointmentStatusUpdateView
)

app_name = "appointments"

urlpatterns = [

    # -----------------------------
    # Create appointment (USER)
    # -----------------------------
    path('create/',AppointmentCreateView.as_view(),name='appointment-create'),

    # -----------------------------
    # User appointments
    # -----------------------------
    path('user/', UserAppointmentListView.as_view(), name='user-appointments'),

    # -----------------------------
    # Advocate appointments
    # -----------------------------
    path('advocate/', AdvocateAppointmentListView.as_view(),name='advocate-appointments'),

    # -----------------------------
    # Update appointment status (ADVOCATE)
    # -----------------------------
    path('update-status/<int:pk>/', AppointmentStatusUpdateView.as_view(),name='appointment-status-update'),
]
