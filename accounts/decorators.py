from django.shortcuts import redirect

def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role != "STUDENT":
            return redirect('login')  # Redirect to home or an appropriate page
        
        return view_func(request, *args, **kwargs)
    
    return wrapper

def teacher_required(view_func):

    def wrapper(
        request,
        *args,
        **kwargs
    ):

        if (
            request.user.role
            != "TEACHER"
        ):

            return redirect(
                "login"
            )

        return view_func(
            request,
            *args,
            **kwargs
        )

    return wrapper

def admin_required(view_func):

    def wrapper(
        request,
        *args,
        **kwargs
    ):

        if (
            request.user.role
            != "ADMIN"
        ):

            return redirect(
                "login"
            )

        return view_func(
            request,
            *args,
            **kwargs
        )

    return wrapper