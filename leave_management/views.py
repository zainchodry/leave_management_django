from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import LeaveRequest
from .forms import LeaveForm, LeaveReviewForm
from accounts.decorators import student_required, teacher_required, admin_required
from notifications.models import Notification


@login_required
@student_required
def apply_leave(request):
    form = LeaveForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        leave = form.save(commit=False)
        leave.student = request.user
        leave.save()
        messages.success(request, "Your leave request has been submitted successfully!")
        return redirect("my_leaves")

    return render(request, "leave_management/apply_leave.html", {"form": form})


@login_required
@student_required
def my_leaves(request):
    leaves = LeaveRequest.objects.filter(student=request.user).order_by("-created_at")
    return render(request, "leave_management/my_leaves.html", {"leaves": leaves})


@login_required
@student_required
def cancel_leave(request, pk):
    leave = get_object_or_404(LeaveRequest, id=pk, student=request.user)

    if leave.status == "PENDING":
        leave.status = "CANCELLED"
        leave.save()
        messages.success(request, "Your leave request has been cancelled.")
    else:
        messages.error(request, "Only pending leaves can be cancelled.")

    return redirect("my_leaves")


@login_required
@teacher_required
def pending_leaves(request):
    leaves = LeaveRequest.objects.filter(status="PENDING").order_by("-created_at")
    return render(request, "leave_management/pending_leaves.html", {"leaves": leaves})


@login_required
@teacher_required
def review_leave(request, pk):
    leave = get_object_or_404(LeaveRequest, id=pk)
    form = LeaveReviewForm(request.POST or None, instance=leave)

    if request.method == "POST" and form.is_valid():
        leave = form.save(commit=False)
        leave.teacher = request.user
        leave.save()

        if leave.status in ["APPROVED", "REJECTED"]:
            Notification.objects.create(
                receiver=leave.student,
                title="Leave Status Updated",
                message=f"Your {leave.get_leave_type_display()} request from {leave.start_date} to {leave.end_date} has been {leave.status.lower()} by {request.user.username}.",
                notification_type="LEAVE_APPROVED" if leave.status == "APPROVED" else "LEAVE_REJECTED",
            )

        messages.success(request, f"Leave request has been {leave.status.lower()}.")
        return redirect("pending_leaves")

    return render(request, "leave_management/leave_detail.html", {"form": form, "leave": leave})


@login_required
@admin_required
def all_leaves(request):
    leaves = LeaveRequest.objects.all().order_by("-created_at")
    return render(request, "leave_management/all_leaves.html", {"leaves": leaves})


@login_required
@admin_required
def delete_leave(request, pk):
    leave = get_object_or_404(LeaveRequest, id=pk)
    leave.delete()
    messages.success(request, "Leave record has been deleted.")
    return redirect("all_leaves")


@login_required
@admin_required
def leave_statistics(request):
    context = {
        "total": LeaveRequest.objects.count(),
        "pending": LeaveRequest.objects.filter(status="PENDING").count(),
        "approved": LeaveRequest.objects.filter(status="APPROVED").count(),
        "rejected": LeaveRequest.objects.filter(status="REJECTED").count(),
        "cancelled": LeaveRequest.objects.filter(status="CANCELLED").count(),
    }
    return render(request, "leave_management/statistics.html", context)
