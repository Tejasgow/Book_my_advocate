from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer
from .permissions import IsClientUser, IsOwnerOrReadOnly


# -----------------------------
# Create Review (Client)
# -----------------------------
class CreateReviewView(APIView):
    permission_classes = [IsAuthenticated, IsClientUser]

    def post(self, request):
        serializer = ReviewCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        review = serializer.save()

        # 🔁 Refresh to get updated advocate rating (after signal)
        review.refresh_from_db()

        return Response(
            {
                "message": "Review submitted successfully ✅",
                "data": ReviewSerializer(review).data
            },
            status=status.HTTP_201_CREATED
        )


# -----------------------------
# List Reviews for an Advocate
# -----------------------------
class AdvocateReviewListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, advocate_id):
        reviews = Review.objects.filter(
            advocate_id=advocate_id
        ).select_related('client', 'advocate')

        avg_rating = reviews.aggregate(
            avg=Avg('rating')
        )['avg'] or 0

        serializer = ReviewSerializer(reviews, many=True)

        return Response({
            "message": "Reviews fetched successfully ✅",
            "average_rating": round(avg_rating, 2),
            "data": serializer.data
        })


# -----------------------------
# Update / Delete Review (Client)
# -----------------------------
class ReviewDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self, pk):
        review = get_object_or_404(Review, pk=pk)
        self.check_object_permissions(self.request, review)
        return review

    def put(self, request, pk):
        review = self.get_object(pk)
        serializer = ReviewCreateSerializer(
            review,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # 🔁 Refresh to reflect updated advocate rating
        review.refresh_from_db()

        return Response({
            "message": "Review updated successfully ✅",
            "data": ReviewSerializer(review).data
        })

    def delete(self, request, pk):
        review = self.get_object(pk)
        review.delete()
        return Response(
            {"message": "Review deleted successfully ✅"},
            status=status.HTTP_204_NO_CONTENT
        )
