from django.urls import path
from .views import (
    AdvocateCreateView,
    AdvocateListView,
    AdvocateDetailView,
    AdvocateUpdateView,
    AdvocateVerifyView,
    AssignAssistantView,
    ListAssistantsView
)

app_name = "advocates"

urlpatterns = [
    # -----------------------------
    # Advocate Profile Endpoints
    # -----------------------------
    path("create/", AdvocateCreateView.as_view(), name="advocate-create"),          # POST: create profile
    path("list/", AdvocateListView.as_view(), name="advocate-list"),               # GET: list verified advocates
    path("detail/<int:pk>/", AdvocateDetailView.as_view(), name="advocate-detail"), # GET: single advocate
    path("update/", AdvocateUpdateView.as_view(), name="advocate-update"),         # PUT: self-update profile
    path("verify/<int:pk>/", AdvocateVerifyView.as_view(), name="advocate-verify"),# POST: admin verify advocate

    # -----------------------------
    # Assistant Lawyer Endpoints
    # -----------------------------
    path("assistant/assign/", AssignAssistantView.as_view(), name="assign-assistant"), # POST: assign assistant
    path("assistant/list/", ListAssistantsView.as_view(), name="list-assistants"),     # GET: list assistants for advocate
]
