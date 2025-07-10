from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BlogForm, BlogForm1
from .models import Post
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

# all posts
def home(request):
    category=request.GET.get('category')
    post=Post.objects.all().order_by('-created_at')

    if category:
        post=post.filter(category=category).order_by('-created_at')
    if not post:
        messages.info(request, "No posts found in this category.")

    return render(request, 'blog/home.html', {
        'posts': post,
        'categories': Post.CATEGORY_CHOICES,
        'selected_category': category
    })

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
                category=form.cleaned_data['category'],
                author=request.user
            )
            return redirect('blog:home') 
    else:
        form = BlogForm()
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def Delete_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        if post.author == request.user or request.user.is_staff:
            post.delete()
            messages.success(request, "Post deleted successfully.")
            return redirect('blog:my_posts')
        else:
            messages.error(request, "You do not have permission to delete this post.")
    except Post.DoesNotExist:
        messages.error(request, "Post not found.")
    return redirect('blog:my_posts')

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

@staff_member_required
def dashboard_create_blog(request):
    if request.method=="POST":
        form=BlogForm1(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            category=form.cleaned_data['category']
            author = form.cleaned_data['author']

      
            Post.objects.create(
                title=title,
                content=content,
                category=category,
                author=author
            )
            messages.success(request, "Blog created successfully.")
            return redirect('/dashboard/blogs/')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BlogForm1()

    return render(request, 'dashboard/blogform.html', {'form': form})

@staff_member_required
def dashboard_edit_blog(request, postid):
    post=Post.objects.get(id=postid)
    if request.method=="POST":
        form=BlogForm1(request.POST, initial={'title':post.title, 'content':post.content, 'author':post.author})
        if form.is_valid():
          title = form.cleaned_data['title']
          content = form.cleaned_data['content']
          author = form.cleaned_data['author']

          post.title=title
          post.content=content
          post.author=author 
          post.save()
          messages.success(request, "Blog updated successfully.")
          return redirect('/dashboard/blogs/')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BlogForm1(initial={'title':post.title, 'content':post.content, 'author':post.author})        

    return render(request, 'dashboard/editblogForm.html', {'form': form, 'post': post}) 

@staff_member_required
def delete_post(request, postid):
    post = Post.objects.get(id=postid)
    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect('/dashboard/blogs/')