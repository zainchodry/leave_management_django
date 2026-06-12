from django.shortcuts import render, redirect
from .models import User, Profile
from .forms import RegisterForm, ProfileForm, CustomPasswordChangeForm
from django.contrib.auth import logout as auth_logout, update_session_auth_hash
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from leave_management.models import LeaveRequest, LeaveBalance
from attendance.models import Attendance
from notifications.models import Notification, Announcement


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        return render(request, 'accounts/register.html', {'form': form})


class PasswordChangeView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        form = CustomPasswordChangeForm(user=request.user)
        return render(request, 'accounts/password_change.html', {'form': form})

    def post(self, request):
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        return render(request, 'accounts/password_change.html', {'form': form})


class ProfileView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        profile = request.user.profile
        form = ProfileForm(instance=profile)
        return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})

    def post(self, request):
        profile = request.user.profile
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})


@login_required
def dashboard(request):
    """Role-based dashboard view."""
    user = request.user
    context = {
        'announcements': Announcement.objects.filter(is_active=True).order_by('-created_at')[:5],
    }

    if user.role == 'STUDENT':
        # Student dashboard
        leaves = LeaveRequest.objects.filter(student=user).order_by('-created_at')
        attendance_records = Attendance.objects.filter(student=user)
        total_attendance = attendance_records.count()
        present_count = attendance_records.filter(status='PRESENT').count()
        attendance_pct = round((present_count / total_attendance) * 100, 1) if total_attendance > 0 else 0

        context.update({
            'recent_leaves': leaves[:5],
            'total_leaves': leaves.count(),
            'pending_leaves': leaves.filter(status='PENDING').count(),
            'approved_leaves': leaves.filter(status='APPROVED').count(),
            'rejected_leaves': leaves.filter(status='REJECTED').count(),
            'attendance_percentage': attendance_pct,
            'total_attendance': total_attendance,
            'present_count': present_count,
            'leave_balances': LeaveBalance.objects.filter(student=user),
        })

    elif user.role == 'TEACHER':
        # Teacher dashboard
        pending_leaves = LeaveRequest.objects.filter(status='PENDING')
        context.update({
            'pending_leaves': pending_leaves[:10],
            'pending_count': pending_leaves.count(),
            'total_reviewed': LeaveRequest.objects.filter(
                teacher=user,
                status__in=['APPROVED', 'REJECTED']
            ).count(),
            'recent_attendance': Attendance.objects.filter(
                marked_by=user
            ).order_by('-created_at')[:10],
        })

    elif user.role == 'ADMIN':
        # Admin dashboard
        context.update({
            'total_users': User.objects.count(),
            'total_students': User.objects.filter(role='STUDENT').count(),
            'total_teachers': User.objects.filter(role='TEACHER').count(),
            'total_leaves': LeaveRequest.objects.count(),
            'pending_leaves': LeaveRequest.objects.filter(status='PENDING').count(),
            'approved_leaves': LeaveRequest.objects.filter(status='APPROVED').count(),
            'rejected_leaves': LeaveRequest.objects.filter(status='REJECTED').count(),
            'total_attendance': Attendance.objects.count(),
            'present_attendance': Attendance.objects.filter(status='PRESENT').count(),
            'absent_attendance': Attendance.objects.filter(status='ABSENT').count(),
        })

    return render(request, 'accounts/dashboard.html', context)


@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')
