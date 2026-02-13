from rest_framework import serializers
from .models import ChatRoom, Message


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.username", read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "sender",
            "sender_name",
            "content",
            "created_at"
        ]
        read_only_fields = ["sender", "created_at"]


class ChatRoomSerializer(serializers.ModelSerializer):
    appointment_id = serializers.IntegerField(source="appointment.id", read_only=True)

    class Meta:
        model = ChatRoom
        fields = ["id", "appointment_id", "created_at"]
