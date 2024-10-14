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
            return HttpResponseForbidden("You do not have permission to access this page.")
    return wrapper

# View that uses the custom decorator
@admin_or_staff_required
def admin_and_staff_page(request):
    return render(request, 'admin_staff_only.html')
