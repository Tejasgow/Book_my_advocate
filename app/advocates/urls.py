from django.urls import path
from .views import AdvocateCreateView, AdvocateListView, AdvocateDetailView

app_name = "advocates"


urlpatterns = [
    # Create Advocate Profile (POST)
    path("create/", AdvocateCreateView.as_view(), name="advocate-create"),

    # List Verified Advocates (GET)
    # Optional query param: ?specialization=Criminal
    path("list/", AdvocateListView.as_view(), name="advocate-list"),

    # Get Single Advocate Profile (GET)
    path("detail/<int:pk>/", AdvocateDetailView.as_view(), name="advocate-detail"),
]
