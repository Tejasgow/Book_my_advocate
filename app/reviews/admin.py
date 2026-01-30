from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'advocate', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'advocate']
    search_fields = ['client__username', 'advocate__user__username', 'comment']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
