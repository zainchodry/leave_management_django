from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages

from .models import Notification, Announcement
from .forms import AnnouncementForm
from accounts.decorators import admin_required


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(receiver=request.user)
    return render(request, "notifications/notification_list.html", {"notifications": notifications})


@login_required
def notification_detail(request, pk):
    notification = get_object_or_404(Notification, pk=pk, receiver=request.user)
    if not notification.is_read:
        notification.is_read = True
        notification.save()
    return render(request, "notifications/notification_detail.html", {"notification": notification})


@login_required
def mark_as_read(request, pk):
    notification = get_object_or_404(Notification, id=pk, receiver=request.user)
    notification.is_read = True
    notification.save()
    return redirect("notification_list")


@login_required
def mark_all_read(request):
    Notification.objects.filter(receiver=request.user, is_read=False).update(is_read=True)
    django_messages.success(request, "All notifications marked as read.")
    return redirect("notification_list")


@login_required
def delete_notification(request, pk):
    notification = get_object_or_404(Notification, id=pk, receiver=request.user)
    notification.delete()
    django_messages.success(request, "Notification deleted.")
    return redirect("notification_list")


@login_required
def announcements(request):
    announcement_list = Announcement.objects.filter(is_active=True)
    return render(request, "notifications/announcements.html", {"announcements": announcement_list})


@login_required
@admin_required
def create_announcement(request):
    form = AnnouncementForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        announcement = form.save(commit=False)
        announcement.created_by = request.user
        announcement.save()
        django_messages.success(request, "Announcement published successfully!")
        return redirect("announcements")
    return render(request, "notifications/create_announcement.html", {"form": form})


@login_required
@admin_required
def delete_announcement(request, pk):
    announcement = get_object_or_404(Announcement, id=pk)
    announcement.delete()
    django_messages.success(request, "Announcement deleted.")
    return redirect("announcements")
