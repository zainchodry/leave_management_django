from django.db import models
from django.conf import settings


class LeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('SICK', 'Sick Leave'),
        ('VACATION', 'Vacation Leave'),
        ('PERSONAL', 'Personal Leave'),
        ('EMERGENCY', 'Emergency Leave'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='leave_requests',
    )
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_leaves',
    )
    teacher_remark = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.username} - {self.leave_type} ({self.start_date} to {self.end_date})"

    @property
    def duration(self):
        """Returns the number of days for this leave request."""
        return (self.end_date - self.start_date).days + 1


class LeaveBalance(models.Model):
    """Tracks how many leave days each student has per leave type."""
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='leave_balances',
    )
    leave_type = models.CharField(max_length=20, choices=LeaveRequest.LEAVE_TYPE_CHOICES)
    total_days = models.PositiveIntegerField(default=10)
    used_days = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('student', 'leave_type')

    def __str__(self):
        return f"{self.student.username} - {self.leave_type}: {self.remaining} remaining"

    @property
    def remaining(self):
        return self.total_days - self.used_days