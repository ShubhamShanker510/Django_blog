from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name="accounts"

urlpatterns=[
    path('register/',register ,name="register"),
    path('login/', login_view, name="login"),
    path('profile/', profile, name="profile" ),
    path('logout/', Logout, name="logout"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete')

]