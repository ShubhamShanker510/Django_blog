from django.shortcuts import redirect
from django.contrib.auth.models import User

class RedirectAdminToDashboardMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/admin/' and request.user.is_authenticated and request.user.is_staff:
            return redirect('/dashboard')

        return self.get_response(request)

class HandleAdminLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.path == '/admin/login/' and
            request.user.is_authenticated and
            (request.user.is_staff or request.user.is_superuser)
        ):
            return redirect('/dashboard')
        
        if (
            request.path == '/admin/login/' and
            request.user.is_authenticated and
            not request.user.is_staff
        ):
            return redirect('/blog/')

        
        return self.get_response(request)