from django.urls import path
from .views import *

app_name = "blog"

urlpatterns = [
    path('', home, name="home"),
    path('create/',create_and_edit_blog, name="create_post"),
    path('post/<int:post_id>/', post_detail, name="post_detail"),
    path('edit/<int:post_id>/', create_and_edit_blog, name="edit_post"),
    path('mypost/', my_posts, name="my_posts"),
    path('delete/<int:post_id>/', Delete_post, name="delete_post"),
]