from django.urls import path
from .views import CreateReviewView, AdvocateReviewListView, ReviewDetailView

urlpatterns = [
    path('reviews/create/', CreateReviewView.as_view(), name='create-review'),
    path('reviews/advocate/<int:advocate_id>/', AdvocateReviewListView.as_view(), name='advocate-reviews'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]
