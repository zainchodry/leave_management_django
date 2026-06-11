from django.db import models
from accounts.models import User

class LeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('SICK', 'Sick Leave'),
        ('VACATION', 'Vacation Leave'),
        ('PERSONAL', 'Personal Leave'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    teacher = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.username} - {self.leave_type} ({self.start_date} to {self.end_date})"
    