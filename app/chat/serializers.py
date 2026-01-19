from rest_framework import serializers
from .models import ChatRoom, Message


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(
        source="sender.username", read_only=True
    )

    class Meta:
        model = Message
        fields = [
            "id",
            "sender",
            "sender_name",
            "text",
            "created_at"
        ]


class ChatRoomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = [
            "id",
            "appointment",
            "messages",
            "created_at"
        ]
