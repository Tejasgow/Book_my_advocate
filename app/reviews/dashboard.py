# reviews/dashboard.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Avg, Count, Q

from .models import Review


class ReviewDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # =================================================
        # ADVOCATE REVIEW DASHBOARD
        # =================================================
        if user.role == "ADVOCATE":
            if not hasattr(user, "advocate_profile"):
                return Response(
                    {"error": "Advocate profile not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            advocate = user.advocate_profile
            reviews = Review.objects.filter(advocate=advocate)

            # Rating distribution
            rating_distribution = reviews.values('rating').annotate(
                count=Count('rating')
            ).order_by('-rating')

            average_rating = reviews.aggregate(
                avg=Avg('rating')
            )['avg'] or 0

            stats = {
                "total_reviews": reviews.count(),
                "average_rating": round(float(average_rating), 2),
                "five_star": reviews.filter(rating=5).count(),
                "four_star": reviews.filter(rating=4).count(),
                "three_star": reviews.filter(rating=3).count(),
                "two_star": reviews.filter(rating=2).count(),
                "one_star": reviews.filter(rating=1).count(),
            }

            # Recent reviews
            recent_reviews = reviews.order_by('-created_at')[:5]
            recent_data = [
                {
                    "id": review.id,
                    "client": review.client.user.first_name,
                    "rating": review.rating,
                    "comment": review.comment[:100] if review.comment else "",
                    "date": review.created_at,
                }
                for review in recent_reviews
            ]

            return Response({
                "role": "ADVOCATE",
                "stats": stats,
                "recent_reviews": recent_data,
                "rating_distribution": list(rating_distribution)
            }, status=status.HTTP_200_OK)

        # =================================================
        # CLIENT REVIEW DASHBOARD
        # =================================================
        elif user.role == "CLIENT":
            if not hasattr(user, "client_profile"):
                return Response(
                    {"error": "Client profile not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            reviews_written = Review.objects.filter(client=user.client_profile)

            stats = {
                "total_reviews_written": reviews_written.count(),
                "five_star_given": reviews_written.filter(rating=5).count(),
                "four_star_given": reviews_written.filter(rating=4).count(),
                "three_star_given": reviews_written.filter(rating=3).count(),
                "two_star_given": reviews_written.filter(rating=2).count(),
                "one_star_given": reviews_written.filter(rating=1).count(),
            }

            # Reviews written by this client
            recent_reviews = reviews_written.order_by('-created_at')[:5]
            recent_data = [
                {
                    "id": review.id,
                    "advocate": review.advocate.user.first_name,
                    "rating": review.rating,
                    "comment": review.comment[:100] if review.comment else "",
                    "date": review.created_at,
                }
                for review in recent_reviews
            ]

            return Response({
                "role": "CLIENT",
                "stats": stats,
                "your_reviews": recent_data
            }, status=status.HTTP_200_OK)

        # =================================================
        # ADMIN REVIEW DASHBOARD
        # =================================================
        elif user.role == "ADMIN":
            reviews = Review.objects.all()

            average_rating = reviews.aggregate(
                avg=Avg('rating')
            )['avg'] or 0

            stats = {
                "total_reviews": reviews.count(),
                "average_system_rating": round(float(average_rating), 2),
                "five_star_reviews": reviews.filter(rating=5).count(),
                "four_star_reviews": reviews.filter(rating=4).count(),
                "three_star_reviews": reviews.filter(rating=3).count(),
                "two_star_reviews": reviews.filter(rating=2).count(),
                "one_star_reviews": reviews.filter(rating=1).count(),
                "unique_advocates_reviewed": reviews.values('advocate').distinct().count(),
                "unique_clients_reviewed": reviews.values('client').distinct().count(),
            }

            return Response({
                "role": "ADMIN",
                "stats": stats
            }, status=status.HTTP_200_OK)

        return Response(
            {"error": "Role not recognized"},
            status=status.HTTP_400_BAD_REQUEST
        )
