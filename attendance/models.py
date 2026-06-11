from django.db import models
from accounts.models import User

class Attendance(models.Model):
    STATUS_CHOICES = (

        ("PRESENT", "Present"),

        ("ABSENT", "Absent"),

        ("LEAVE", "Leave"),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attendance")
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="marked_attendance")
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Mate:
        uniwue_together = ("student", "date")

        ordering = ["-date"]

    def __str__(self):
        return f"{self.student.username} - {self.date} - {self.status}"

