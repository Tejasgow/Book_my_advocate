from django.urls import path
from . import views

urlpatterns = [
    # -----------------------------
    # Client Profile
    # -----------------------------
    path('profile/', views.ClientProfileView.as_view(), name='client-profile'),
    path('profile/update/', views.ClientProfileUpdateView.as_view(), name='client-profile-update'),

    # -----------------------------
    # Appointments
    # -----------------------------
    path('appointments/', views.ClientAppointmentsView.as_view(), name='client-appointments'),

    # -----------------------------
    # Cases
    # -----------------------------
    path('cases/', views.ClientCasesView.as_view(), name='client-cases'),
    path('cases/<int:pk>/', views.ClientCaseDetailView.as_view(), name='client-case-detail'),

    # -----------------------------
    # Case Hearings
    # -----------------------------
    path('cases/<int:case_id>/hearings/', views.ClientCaseHearingsView.as_view(), name='client-case-hearings'),

    # -----------------------------
    # Case Documents
    # -----------------------------
    path('cases/<int:case_id>/documents/', views.ClientCaseDocumentsView.as_view(), name='client-case-documents'),
]
