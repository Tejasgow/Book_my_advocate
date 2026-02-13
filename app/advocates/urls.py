from django.urls import path
from .dashboard import AdvocateDashboardView
from .views import (
    AdvocateCreateView,
    AdvocateListView,
    AdvocateDetailView,
    AdvocateUpdateView,
    AdvocateUploadOfficialIDView,
    AdvocateVerifyView,
    AssignAssistantView,
    ListAssistantsView,
    
)

urlpatterns = [

    # -------------------------------------------------
    # Advocate Profile APIs
    # -------------------------------------------------
    # Create advocate profile (ADVOCATE only, once)
    path("profiles/create/",AdvocateCreateView.as_view(),name="advocate-profile-create"),

    # List all VERIFIED advocate profiles (Public / Read-only)
    path("profiles/",AdvocateListView.as_view(),name="advocate-profile-list"),

    # Retrieve single advocate profile by ID (Public / Read-only)
    path("profiles/<int:pk>/",AdvocateDetailView.as_view(),name="advocate-profile-detail"),

    # Update logged-in advocate’s OWN profile (No ID in URL)
    path("profiles/update/",AdvocateUpdateView.as_view(),name="advocate-profile-update"),

    # -------------------------------------------------
    # Verification
    # -------------------------------------------------
    path("profiles/upload-id/",AdvocateUploadOfficialIDView.as_view(),name="advocate-upload-id"),

    path("profiles/<int:pk>/verify/",AdvocateVerifyView.as_view(),name="advocate-verify"),

    # -------------------------------------------------
    # Assistant Lawyers
    # -------------------------------------------------

    path("assistants/assign/",AssignAssistantView.as_view(),name="assistant-assign"),

    path("assistants/",ListAssistantsView.as_view(),name="assistant-list"),

    # -------------------------------------------------
    # Advocate dashboard
    # -------------------------------------------------

    path("dashboard/advocate/", AdvocateDashboardView.as_view(), name="advocate-dashboard"),
]
