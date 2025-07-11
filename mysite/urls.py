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
from accounts.views import  dashboard_blog_view, dashboard_user_view, dashboard_home_view, dashboard_profile_view, dashboard_logout,dashboard_create_edit_user, delete_user, dashboard_categories_view, redirect_to_custom_dashboard
from accounts.admin import custom_admin_site
from blog.views import dashboard_create_edit_blog, delete_post, dashboard_create_category, dashboard_delete_category, dashboard_delete_category_view
urlpatterns = [
    path('admin/', custom_admin_site.urls), 
    path('dashboard/',dashboard_home_view, name='custom_admin_dashboard'),
    path('dashboard/blogs/', dashboard_blog_view, name='dashboard_blog'),
    path('dashboard/users/', dashboard_user_view, name='dashboard_user'),
    path('dashboard/categories/', dashboard_categories_view, name='dashboard_categories'),
    path('dashboard/create-category/', dashboard_create_category, name='dashboard_create_category'),
    path('dashboard/delete-category/', dashboard_delete_category_view, name='dashboard_delete_category_view'),
    path('dashboard/delete-category/<int:category_id>/', dashboard_delete_category, name='dashboard_delete_category'),
    path('dashboard/profile/', dashboard_profile_view, name='dashboard_profile'),
    path('dashboard/logout/', dashboard_logout, name='dashboard_logout'),
    path('dashboard/create-user/',dashboard_create_edit_user, name='dashboard_create_user'),
    path('dashboard/create-blog/', dashboard_create_edit_blog, name='dashboard_create_blog'),
    path('dashboard/edit-user/<int:user_id>/', dashboard_create_edit_user, name='edit_user'),
    path('dashboard/delete-user/<int:userid>/', delete_user, name='delete_user'),
    path('dashboard/edit-post/<int:post_id>/', dashboard_create_edit_blog, name='edit_post'),
    path('dashboard/delete-post/<int:postid>/', delete_post, name='delete_post'),
    path('blog/', include("blog.urls", namespace="blog")),
    path('accounts/', include("accounts.urls", namespace="accounts")),
    path('accounts/', include('django.contrib.auth.urls')),
]
