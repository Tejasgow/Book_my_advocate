from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from app.appointments.models import Appointment
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer

# -----------------------------
# Create or Get Chat Room
# -----------------------------
class CreateOrGetChatRoom(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id)

        # ✅ Allow only approved or completed appointments
        if appointment.status not in ["APPROVED", "COMPLETED"]:
            return Response(
                {"error": "Chat allowed only for approved or completed appointments"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🔐 Authorization check
        if not is_chat_user(request.user, appointment):
            return Response(
                {"error": "You are not authorized to access this chat"},
                status=status.HTTP_403_FORBIDDEN
            )

        room, _ = ChatRoom.objects.get_or_create(appointment=appointment)

        return Response(
            {
                "message": "Chat room fetched successfully ✅",
                "data": ChatRoomSerializer(room).data
            },
            status=status.HTTP_200_OK
        )

def is_chat_user(user, appointment):
    return (
        appointment.client.user == user or
        appointment.advocate.user == user
    )

# -----------------------------
# Send Message
# -----------------------------
class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        room = get_object_or_404(
            ChatRoom.objects.select_related("appointment"),
            id=room_id
        )

        # 🔐 Authorization
        if not is_chat_user(request.user, room.appointment):
            return Response(
                {"error": "You are not allowed to send messages here"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(
            room=room,
            sender=request.user
        )

        return Response(
            {
                "message": "Message sent successfully ✅",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


# -----------------------------
# Get All Messages in a Room
# -----------------------------
class GetMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        room = get_object_or_404(
            ChatRoom.objects.select_related("appointment"),
            id=room_id
        )

        # 🔐 Authorization
        if not is_chat_user(request.user, room.appointment):
            return Response(
                {"error": "You are not allowed to view these messages"},
                status=status.HTTP_403_FORBIDDEN
            )

        messages = room.messages.select_related("sender").order_by("created_at")

        return Response(
            {
                "message": "Messages fetched successfully ✅",
                "data": MessageSerializer(messages, many=True).data
            },
            status=status.HTTP_200_OK
        )
