from django.shortcuts import redirect
from functools import wraps


def student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.role != "STUDENT":
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def teacher_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.role != "TEACHER":
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.role != "ADMIN":
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper