from django.contrib.admin import AdminSite
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from django.urls import path
from .views import AdminLoginRedirectView

class MyAdminSite(AdminSite):

    def islogin(self, request, extra_context=None):
        if request.user.is_authenticated:
            return redirect('/dashboard/')
        return super().login(request, extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('login/', AdminLoginRedirectView.as_view(), name='login'),
        ]
        return custom_urls + urls

custom_admin_site = MyAdminSite(name='myadmin')