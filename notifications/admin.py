from django.contrib import admin
from .models import Notification, Announcement


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("receiver", "title", "notification_type", "is_read", "created_at")
    list_filter = ("notification_type", "is_read")
    search_fields = ("receiver__email", "title")
    ordering = ("-created_at",)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "content")
    ordering = ("-created_at",)