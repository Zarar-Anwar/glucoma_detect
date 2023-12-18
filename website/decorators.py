from functools import wraps
from django.shortcuts import redirect


def user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_user:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('user-login')

    return _wrapped_view


def doctor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_doctor:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('user-login')

    return _wrapped_view
