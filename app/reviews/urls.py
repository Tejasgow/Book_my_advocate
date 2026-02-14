from django.urls import path
from .views import CreateReviewView, AdvocateReviewListView, ReviewDetailView
from .dashboard import ReviewDashboardView

urlpatterns = [
    path('reviews/create/', CreateReviewView.as_view(), name='create-review'),
    path('reviews/advocate/<int:advocate_id>/', AdvocateReviewListView.as_view(), name='advocate-reviews'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),

    # =================================================
    # DASHBOARD
    # =================================================
    path('dashboard/', ReviewDashboardView.as_view(), name='dashboard'),
]
