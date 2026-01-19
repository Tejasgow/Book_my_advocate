from django.urls import path
from .views import CreateOrGetChatRoom, SendMessageView, GetMessagesView

app_name = "chat"

urlpatterns = [
    # Create or fetch a chat room for a specific appointment
    path("room/<int:appointment_id>/", CreateOrGetChatRoom.as_view(), name="create_or_get_room"),

    # Send a message to a specific chat room
    path("room/<int:room_id>/send/", SendMessageView.as_view(), name="send_message"),

    # Get all messages in a chat room
    path("room/<int:room_id>/messages/", GetMessagesView.as_view(), name="get_messages"),
]
