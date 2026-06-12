from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Attendance
from .forms import AttendanceForm, AttendanceUpdateForm
from accounts.decorators import teacher_required, student_required, admin_required


@login_required
@teacher_required
def mark_attendance(request):
    form = AttendanceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        attendance = form.save(commit=False)
        attendance.marked_by = request.user
        attendance.save()
        messages.success(request, "Attendance marked successfully!")
        return redirect("mark_attendance")
    return render(request, "attendance/mark_attendance.html", {"form": form})


@login_required
@teacher_required
def update_attendance(request, pk):
    attendance = get_object_or_404(Attendance, id=pk)
    form = AttendanceUpdateForm(request.POST or None, instance=attendance)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Attendance updated successfully!")
        return redirect("all_attendance")
    return render(request, "attendance/update_attendance.html", {"form": form, "attendance": attendance})


@login_required
@student_required
def my_attendance(request):
    records = Attendance.objects.filter(student=request.user).order_by("-date")
    total = records.count()
    present = records.filter(status="PRESENT").count()
    absent = records.filter(status="ABSENT").count()
    percentage = round((present / total) * 100, 1) if total > 0 else 0

    return render(request, "attendance/my_attendance.html", {
        "records": records,
        "total": total,
        "present": present,
        "absent": absent,
        "percentage": percentage,
    })


@login_required
@admin_required
def all_attendance(request):
    attendance = Attendance.objects.all().order_by("-date")
    return render(request, "attendance/all_attendance.html", {"attendance": attendance})


@login_required
@admin_required
def attendance_statistics(request):
    context = {
        "total": Attendance.objects.count(),
        "present": Attendance.objects.filter(status="PRESENT").count(),
        "absent": Attendance.objects.filter(status="ABSENT").count(),
        "leave": Attendance.objects.filter(status="LEAVE").count(),
    }
    return render(request, "attendance/attendance_statistics.html", context)


@login_required
@admin_required
def delete_attendance(request, pk):
    attendance = get_object_or_404(Attendance, id=pk)
    attendance.delete()
    messages.success(request, "Attendance record deleted.")
    return redirect("all_attendance")
