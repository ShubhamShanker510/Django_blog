from django.shortcuts import redirect


class RedirectAdminToDashboardMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/admin/' and request.user.is_authenticated and request.user.is_staff:
            return redirect('/dashboard')

        return self.get_response(request)

