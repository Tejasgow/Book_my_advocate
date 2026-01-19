from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from app.appointments.models import Appointment
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer


# -----------------------------
# Create or Get Chat Room
# -----------------------------
class CreateOrGetChatRoom(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

        # ✅ Allow chat only if appointment is APPROVED or COMPLETED
        if appointment.status not in ["APPROVED", "COMPLETED"]:
            return Response(
                {"error": "Chat allowed only for approved or completed appointments"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create or get the chat room
        room, created = ChatRoom.objects.get_or_create(appointment=appointment)

        serializer = ChatRoomSerializer(room)
        return Response(
            {"message": "Chat room fetched successfully ✅", "data": serializer.data},
            status=status.HTTP_200_OK
        )


# -----------------------------
# Send Message
# -----------------------------
class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        try:
            room = ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return Response({"error": "Chat room not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(room=room, sender=request.user)
            return Response(
                {"message": "Message sent ✅", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------
# Get All Messages in a Room
# -----------------------------
class GetMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        try:
            room = ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return Response({"error": "Chat room not found"}, status=status.HTTP_404_NOT_FOUND)

        messages = room.messages.order_by("created_at")
        serializer = MessageSerializer(messages, many=True)

        return Response(
            {"message": "Messages fetched successfully ✅", "data": serializer.data},
            status=status.HTTP_200_OK
        )
