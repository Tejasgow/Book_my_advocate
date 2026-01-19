from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import ChatRoom, Message

# -----------------------------
# Message Inline for ChatRoom
# -----------------------------
class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('sender_link', 'text', 'created_at')
    ordering = ('created_at',)

    def sender_link(self, obj):
        url = reverse("admin:accounts_user_change", args=[obj.sender.id])
        return format_html('<a href="{}">{}</a>', url, obj.sender.username)
    sender_link.short_description = 'Sender'

# -----------------------------
# ChatRoom Admin
# -----------------------------
@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'appointment_link', 'created_at')
    search_fields = ('appointment__id', 'appointment__user__username', 'appointment__advocate__user__username')
    inlines = [MessageInline]

    def appointment_link(self, obj):
        url = reverse("admin:appointments_appointment_change", args=[obj.appointment.id])
        return format_html('<a href="{}">Appointment #{}</a>', url, obj.appointment.id)
    appointment_link.short_description = 'Appointment'

# -----------------------------
# Message Admin
# -----------------------------
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_link', 'sender_link', 'short_text', 'created_at')
    list_filter = ('room', 'sender')
    search_fields = ('sender__username', 'text')
    readonly_fields = ('created_at',)

    def room_link(self, obj):
        url = reverse("admin:chat_chatroom_change", args=[obj.room.id])
        return format_html('<a href="{}">Room #{}</a>', url, obj.room.id)
    room_link.short_description = 'Room'

    def sender_link(self, obj):
        url = reverse("admin:accounts_user_change", args=[obj.sender.id])
        return format_html('<a href="{}">{}</a>', url, obj.sender.username)
    sender_link.short_description = 'Sender'

    def short_text(self, obj):
        return obj.text if len(obj.text) < 50 else obj.text[:47] + '...'
    short_text.short_description = 'Message'
