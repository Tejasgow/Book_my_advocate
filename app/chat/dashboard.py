# chat/dashboard.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Count, Q

from .models import ChatRoom, Message


class ChatDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # =================================================
        # ADVOCATE CHAT DASHBOARD
        # =================================================
        if user.role == "ADVOCATE":
            if not hasattr(user, "advocate_profile"):
                return Response(
                    {"error": "Advocate profile not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            advocate = user.advocate_profile
            
            # Get all chat rooms for appointments with this advocate
            chat_rooms = ChatRoom.objects.filter(
                appointment__advocate=advocate
            )

            stats = {
                "total_chat_rooms": chat_rooms.count(),
                "active_chats": chat_rooms.exclude(messages__isnull=True).distinct().count(),
                "total_messages_sent": Message.objects.filter(
                    sender=user,
                    room__appointment__advocate=advocate
                ).count(),
                "total_messages_received": Message.objects.exclude(
                    sender=user
                ).filter(
                    room__appointment__advocate=advocate
                ).count(),
            }

            # Recent chats
            recent_chats = chat_rooms.annotate(
                message_count=Count('messages')
            ).order_by('-appointment__appointment_date')[:5]

            recent_data = [
                {
                    "room_id": chat.id,
                    "client": chat.appointment.client.user.first_name,
                    "messages_count": chat.message_count,
                    "created_at": chat.created_at,
                }
                for chat in recent_chats
            ]

            return Response({
                "role": "ADVOCATE",
                "stats": stats,
                "recent_chats": recent_data
            }, status=status.HTTP_200_OK)

        # =================================================
        # CLIENT CHAT DASHBOARD
        # =================================================
        elif user.role == "CLIENT":
            if not hasattr(user, "client_profile"):
                return Response(
                    {"error": "Client profile not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            client = user.client_profile
            
            # Get all chat rooms for appointments with this client
            chat_rooms = ChatRoom.objects.filter(
                appointment__client=client
            )

            stats = {
                "total_chat_rooms": chat_rooms.count(),
                "active_chats": chat_rooms.exclude(messages__isnull=True).distinct().count(),
                "total_messages_sent": Message.objects.filter(
                    sender=user,
                    room__appointment__client=client
                ).count(),
                "total_messages_received": Message.objects.exclude(
                    sender=user
                ).filter(
                    room__appointment__client=client
                ).count(),
            }

            # Recent chats
            recent_chats = chat_rooms.annotate(
                message_count=Count('messages')
            ).order_by('-appointment__appointment_date')[:5]

            recent_data = [
                {
                    "room_id": chat.id,
                    "advocate": chat.appointment.advocate.user.first_name,
                    "messages_count": chat.message_count,
                    "created_at": chat.created_at,
                }
                for chat in recent_chats
            ]

            return Response({
                "role": "CLIENT",
                "stats": stats,
                "recent_chats": recent_data
            }, status=status.HTTP_200_OK)

        # =================================================
        # ADMIN CHAT DASHBOARD
        # =================================================
        elif user.role == "ADMIN":
            chat_rooms = ChatRoom.objects.all()
            messages = Message.objects.all()

            stats = {
                "total_chat_rooms": chat_rooms.count(),
                "total_messages": messages.count(),
                "active_chats": chat_rooms.exclude(messages__isnull=True).distinct().count(),
                "unique_senders": messages.values('sender').distinct().count(),
            }

            return Response({
                "role": "ADMIN",
                "stats": stats
            }, status=status.HTTP_200_OK)

        return Response(
            {"error": "Role not recognized"},
            status=status.HTTP_400_BAD_REQUEST
        )
