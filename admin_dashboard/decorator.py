from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Custom decorator for admin and staff access
def admin_or_staff_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
             return render(request, 'admin_staff_only.html')
    return wrapper
