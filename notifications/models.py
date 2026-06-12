from django.db import models
from django.conf import settings


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ("LEAVE_APPLIED", "Leave Applied"),
        ("LEAVE_APPROVED", "Leave Approved"),
        ("LEAVE_REJECTED", "Leave Rejected"),
        ("ATTENDANCE_MARKED", "Attendance Marked"),
        ("ANNOUNCEMENT", "Announcement"),
        ("GENERAL", "General"),
    )

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=50,
        choices=NOTIFICATION_TYPES,
        default="GENERAL",
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.receiver.email} - {self.title}"


class Announcement(models.Model):
    """System-wide announcements created by admins."""
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="announcements",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
