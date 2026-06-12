from django.contrib import admin
from .models import LeaveRequest, LeaveBalance


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'leave_type', 'start_date', 'end_date', 'status', 'teacher', 'created_at')
    list_filter = ('status', 'leave_type', 'created_at')
    search_fields = ('student__email', 'student__username', 'reason')
    ordering = ('-created_at',)


@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'leave_type', 'total_days', 'used_days', 'remaining')
    list_filter = ('leave_type',)
    search_fields = ('student__email', 'student__username')

    def remaining(self, obj):
        return obj.remaining
    remaining.short_description = 'Remaining Days'
