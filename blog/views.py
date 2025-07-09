from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BlogForm
from .models import Post
from django.contrib import messages

# Create your views here.

# all posts
def home(request):
    post=Post.objects.all().order_by('-created_at')
    return render(request, 'blog/home.html', {'posts': post})


#show a single post
def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        messages.error(request, "Post not found.")
        return redirect('blog:home')
    
    return render(request, 'blog/post_detail.html', {'post': post})


#create a new post
@login_required
def create_post(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            post = Post.objects.create(
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                author=request.user
            )
            return redirect('blog:home') 
    else:
        form = BlogForm()
    return render(request, 'blog/create_post.html', {'form': form})




@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        form = BlogForm(request.POST, initial={'title': post.title, 'content': post.content})
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.save()
            return redirect('blog:home')
    else:
        form = BlogForm(initial={'title': post.title, 'content': post.content})
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

#Show my posts
@login_required
def my_posts(request):
    user = request.user
    posts = Post.objects.filter(author=user).order_by('-created_at')
    return render(request, 'blog/my_posts.html', {'posts': posts})