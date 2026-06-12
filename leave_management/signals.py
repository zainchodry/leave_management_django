from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import LeaveRequest, LeaveBalance
from notifications.models import Notification
from accounts.models import User


@receiver(post_save, sender=LeaveRequest)
def leave_applied_notification(sender, instance, created, **kwargs):
    """Notify all teachers when a new leave request is submitted."""
    if created:
        teachers = User.objects.filter(role="TEACHER")
        for teacher in teachers:
            Notification.objects.create(
                receiver=teacher,
                title="New Leave Request",
                message=f"{instance.student.username} applied for {instance.get_leave_type_display()} from {instance.start_date} to {instance.end_date}.",
                notification_type="LEAVE_APPLIED",
            )


@receiver(post_save, sender=LeaveRequest)
def update_leave_balance(sender, instance, **kwargs):
    """Update leave balance when a leave is approved or cancelled."""
    if instance.status == "APPROVED":
        balance, _ = LeaveBalance.objects.get_or_create(
            student=instance.student,
            leave_type=instance.leave_type,
            defaults={'total_days': 10, 'used_days': 0},
        )
        duration = instance.duration
        if balance.used_days + duration <= balance.total_days:
            balance.used_days += duration
            balance.save()


@receiver(post_save, sender=User)
def create_leave_balances(sender, instance, created, **kwargs):
    """Create default leave balances for new student accounts."""
    if created and instance.role == "STUDENT":
        for leave_type, _ in LeaveRequest.LEAVE_TYPE_CHOICES:
            LeaveBalance.objects.get_or_create(
                student=instance,
                leave_type=leave_type,
                defaults={'total_days': 10, 'used_days': 0},
            )
