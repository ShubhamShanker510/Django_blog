from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BlogForm, DashboardBlogForm, CreateCategoryForm
from .models import Post, Category
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

def redirect_to_blogs(request):
    return redirect('/blog/')

# all posts
def home(request):
    category=request.GET.get('category')
    post=Post.objects.all().order_by('-created_at')

    if category:
        post=post.filter(category=category).order_by('-created_at')
    if not post:
        messages.info(request, "No posts found in this category.")

    categorychoices= Category.objects.values_list('id', 'name')
    return render(request, 'blog/home.html', {
        'posts': post,
        'categories': categorychoices,
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


@login_required
def Delete_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        if post.author == request.user or request.user.is_staff:
            post.delete()
            messages.warning(request, "Post deleted successfully.")
            return redirect('blog:my_posts')
        else:
            messages.error(request, "You do not have permission to delete this post.")
    except Post.DoesNotExist:
        messages.error(request, "Post not found.")
    return redirect('blog:my_posts')

#create and edit post
@login_required
def create_and_edit_blog(request, post_id=None):
    post=get_object_or_404(Post, id=post_id) if post_id else None
    
    if request.method=="POST":
        form=BlogForm(request.POST, instance=post)
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.author=request.user
            new_post.save()

            if post_id:
                messages.success(request,"Blog Updated successfully")
            else:
                messages.success(request, "blog created successfully")

            return redirect('blog:home')

    else:
        form = BlogForm(instance=post)
    return render(request, 'blog/create_edit_post.html', {'post':post, 'form':form})



#Show my posts
@login_required
def my_posts(request):
    user = request.user
    posts = Post.objects.filter(author=user).order_by('-created_at')
    return render(request, 'blog/my_posts.html', {'posts': posts})

@staff_member_required
def dashboard_create_edit_blog(request, post_id=None):
    post=get_object_or_404(Post, id=post_id) if post_id else None

    if request.method=="POST":
        form=DashboardBlogForm(request.POST, instance=post)
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.save()
            
            if post_id:
                messages.success(request,"Blog updated successfully")
            else:
                messages.success(request, "Blog created successfully")

            return redirect('/dashboard/blogs')
        else:
            messages.error("Something went wrong")
    else:
        form=DashboardBlogForm(instance=post)

    return render(request, 'dashboard/create_edit_blog.html', {'form':form, 'post':post})


@staff_member_required
def delete_post(request, postid):
    post = Post.objects.get(id=postid)
    post.delete()
    messages.WARNING(request, "Post deleted successfully.")
    return redirect('/dashboard/blogs/')


@staff_member_required
def dashboard_create_category(request):
    if request.method=="POST":
        names=request.POST.getlist("name")
        created_any=False
        already_exists=[]

        for name in names:
            name=name.strip()

            if name:
                category,created=Category.objects.get_or_create(name=name)
                if created:
                    created_any=True
                else:
                    already_exists.append(name)
        if created_any:
            messages.success(request, "New categories added successfully.")
        if already_exists:
            messages.info(request, f"These categories already exist: {', '.join(already_exists)}")

        return redirect('/dashboard/categories/')
    
    return render(request, 'dashboard/categoryform.html')

@staff_member_required
def dashboard_delete_category_view(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/deletecategory.html', {'categories': categories})  

@staff_member_required
def dashboard_delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        messages.success(request, "Category deleted successfully.")
        
    except Category.DoesNotExist:
        messages.error(request, "Category not found.")
    return redirect('/dashboard/delete-category/')

@staff_member_required
def clear_filter_search_blog(request):
    selected_title=request.GET.get('title', '').strip()
    selected_category=request.GET.get('category', '')

    if not selected_category and not selected_title:
        return redirect('/dashboard/blogs')
    
    try:
        blogs=Post.objects.all()
        messages.success(request,"All Blogs shown successfully")
        return redirect('/dashboard/blogs')
    except Post.DoesNotExist:
        messages.error(request, "No blogs found")
        
    