from django.urls import path
from .views import (
    AppointmentCreateView,
    ClientAppointmentListView,
    AppointmentStatusUpdateView,
    AppointmentCancelView,
    AppointmentDetailView,
    AppointmentUpdateView,
)

urlpatterns = [

    # =================================================
    # CLIENT APPOINTMENT ENDPOINTS
    # =================================================

    # List all client appointments
    path(
        'client/appointments/',
        ClientAppointmentListView.as_view(),
        name='client-appointment-list'
    ),

    # Create appointment
    path(
        'client/appointments/create/',
        AppointmentCreateView.as_view(),
        name='client-appointment-create'
    ),

    # Get appointment detail
    path(
        'client/appointments/<int:pk>/',
        AppointmentDetailView.as_view(),
        name='client-appointment-detail'
    ),

    # Update / Reschedule appointment
    path(
        'client/appointments/<int:pk>/update/',
        AppointmentUpdateView.as_view(),
        name='client-appointment-update'
    ),

    # Cancel appointment
    path(
        'client/appointments/<int:pk>/cancel/',
        AppointmentCancelView.as_view(),
        name='client-appointment-cancel'
    ),

    # =================================================
    # ADVOCATE APPOINTMENT ENDPOINTS
    # =================================================

    # Approve / Reject / Complete appointment
    path(
        'advocate/appointments/<int:pk>/status/',
        AppointmentStatusUpdateView.as_view(),
        name='advocate-appointment-status'
    ),
]
