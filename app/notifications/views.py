from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Notification
from .serializers import NotificationSerializer
from app.accounts.models import User


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(
            user=request.user
        ).order_by("-created_at")

        serializer = NotificationSerializer(notifications, many=True)

        unread_count = notifications.filter(is_read=False).count()

        return Response({
            "unread_count": unread_count,
            "notifications": serializer.data
        }, status=status.HTTP_200_OK)


class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        notification = get_object_or_404(
            Notification,
            pk=pk,
            user=request.user
        )

        notification.is_read = True
        notification.save()

        return Response(
            {"message": "Notification marked as read ✅"},
            status=status.HTTP_200_OK
        )

class CreateNotificationView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        user_id = request.data.get("user_id")
        title = request.data.get("title")
        message = request.data.get("message")
        notification_type = request.data.get("notification_type", "SYSTEM")

        if not all([user_id, title, message]):
            return Response(
                {"error": "user_id, title, message required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, id=user_id)

        Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type
        )

        return Response(
            {"message": "Notification sent successfully ✅"},
            status=status.HTTP_201_CREATED
        )
