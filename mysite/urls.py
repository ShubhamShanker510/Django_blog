"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.views import  dashboard_blog_view, dashboard_user_view, dashboard_home_view, dashboard_profile_view, dashboard_logout
from accounts.admin import custom_admin_site
urlpatterns = [
    path('admin/', custom_admin_site.urls), 
    path('dashboard/',dashboard_home_view, name='custom_admin_dashboard'),
    path('dashboard/blogs/', dashboard_blog_view, name='dashboard_blog'),
    path('dashboard/users/', dashboard_user_view, name='dashboard_user'),
    path('dashboard/profile/', dashboard_profile_view, name='dashboard_profile'),
    path('dashboard/logout/', dashboard_logout, name='dashboard_logout'),
    path('blog/', include("blog.urls", namespace="blog")),
    path('accounts/', include("accounts.urls", namespace="accounts")),
    path('accounts/', include('django.contrib.auth.urls')),
]
