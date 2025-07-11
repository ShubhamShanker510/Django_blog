from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from .forms import registrationForm, loginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from blog.models import Post
from blog.forms import DashboardBlogForm
from blog.models import Category
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
# Create your views here.

#User registration
def register(request):
    if request.user.is_authenticated:
        return redirect('/blog/')
    if request.method=="POST":
        form=registrationForm(request.POST)

        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "User registered successfully")
            return redirect('/accounts/login')
        
        else:
            messages.error(request, "Something went wrong")

    else:
        form=registrationForm()

    return render(request, 'accounts/register.html', {"form":form})

@login_required
def redirect_to_custom_dashboard(request):
    if request.user.is_staff:
        return redirect('/dashboard/')
    else:
        return redirect('/admin/')

class AdminLoginRedirectView(LoginView):
    template_name = 'admin/login.html'  # Use Django’s default admin template
    redirect_authenticated_user = True  # Optional, if user is already logged in

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('dashboard_user') 
        return super().get_success_url()

@staff_member_required
def adminlte_dashboard(request):
    redirect('/accounts/adminlte-dashboard/home')
    return render(request, 'dashboard_base.html')

@staff_member_required
def dashboard_blog_view(request):

    selected_title=request.GET.get('title','').strip()
    selected_category=request.GET.get('category','')
    blog_qs=Post.objects.all()

    if selected_title and selected_category:
        blog_qs = Post.objects.filter(title__icontains=selected_title, category__id=selected_category)
    elif selected_title:
        blog_qs=Post.objects.filter(title__icontains=selected_title)
    elif selected_category:
        blog_qs=Post.objects.filter(category__id=selected_category)

    blog=blog_qs.order_by('-created_at')
    paginator=Paginator(blog, 5)
    page_number=request.GET.get('page')
    page=paginator.get_page(page_number)
    blogCount=blog_qs.count()

    form = DashboardBlogForm()
    category_choices = form.fields['category'].queryset
    return render(request, 'dashboard/blog.html', {'blogs':page, 'page_obj':page,'blogCount':blogCount, 'selected_title':selected_title, 'selected_category':selected_category, 'categories': category_choices,})

@staff_member_required
def dashboard_user_view(request):
    selected_username = request.GET.get('username', '').strip()
    selected_email = request.GET.get('email', '').strip()

    user_qs = User.objects.filter(is_superuser=False)

    if selected_username:
        user_qs = user_qs.filter(username__icontains=selected_username)
    if selected_email:
        user_qs = user_qs.filter(email__icontains=selected_email)

    users = user_qs.order_by("-date_joined")
    paginator=Paginator(users, 5)
    page_number=request.GET.get('page')
    page=paginator.get_page(page_number)
    usercount=User.objects.all().count()

    return render(request, 'dashboard/user.html', {
        'users': page,
        'page_obj':page,
        'usercount':usercount,
        'selected_username': selected_username,
        'selected_email': selected_email,
    })


@staff_member_required
def dashboard_home_view(request):
    if request.user.is_authenticated:
        user = request.user
        total_blogs = Post.objects.count()
        total_users = User.objects.count()
        context = {
            'user': user,
            'total_blogs': total_blogs,
            'total_users': total_users
        }
        return render(request, 'dashboard/home.html', context)
    return render(request, 'dashboard/home.html')

@staff_member_required
def dashboard_profile_view(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'dashboard/profile.html', {'user': user})
    


#User login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/blog/')
    
    if request.method=="POST":
        form=loginForm(request.POST)

        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']

            
            user=authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request,"User login successfully")
                return redirect('/blog/')
            else:
                messages.error(request, "Invalid user")

           
        
    else:
        form=loginForm()

    return render(request, 'accounts/login.html', {'form': form})


# user profile
@login_required
def profile(request):
    user=request.user
    return render(request, 'accounts/profile.html', {'user':user})

#logout user
@login_required
def Logout(request):
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect('accounts:login')




@staff_member_required
def dashboard_logout(request):
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect('/admin/')

@staff_member_required
def delete_user(request,userid):
    user=User.objects.get(id=userid)
    user.delete()
    messages.success(request, "User deleted successfully")
    return redirect('/dashboard/users')
        
@staff_member_required
def dashboard_categories_view(request):
    form=DashboardBlogForm()
    category = request.GET.get('category')
    authorid = request.GET.get('author')
    print("category:", category)
    print("authordid:", authorid)
    if category and authorid:
        blogs = Post.objects.filter(category=category, author_id=authorid).order_by('-created_at')
        messages.success(request, f"Filtered blogs by category: {category} and author: {authorid}")
    elif category:
        blogs=Post.objects.filter(category=category).order_by('created_at')
        messages.success(request, f"Filtered blogs by category: {category}")
    elif authorid:
        blogs = Post.objects.filter(author_id=authorid).order_by('-created_at')
        messages.success(request, f"Filtered blogs by author: {authorid}")
    elif category is None and authorid is None:
        blogs = Post.objects.all().order_by('-created_at')
    else:
        blogs = Post.objects.all().order_by('-created_at')

    paginator=Paginator(blogs, 5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    categoryCount=Post.objects.all().count()
    
    categorychoices= Category.objects.values_list('id', 'name')
    authorchoices=form
    return render(request, 'dashboard/categories.html', {'blogs': page_obj,'page_obj':page_obj, 'categoryCount': categoryCount, 'authorchoices': authorchoices,'categorychoices': categorychoices, 'selected_category': category, 'selected_author': authorid})

@staff_member_required
def dashboard_create_edit_user(request, user_id=None):
    user=get_object_or_404(User, id=user_id) if user_id else None

    if request.method=="POST":
        form=registrationForm(request.POST, instance=user)

        if form.is_valid():
            new_user=form.save(commit=False)
            new_password=form.cleaned_data.get('new_password')

            if new_password:
                new_user.set_password(new_password)

            new_user.save()


            if user_id:
                messages.success(request,"User updated successfully")
            else:
                messages.success(request,"User created successfully")
            return redirect('/dashboard/users/')
        else:
            messages.error(request,"Something went wrong")
    else:
        form=registrationForm(instance=user)
    return render(request, 'dashboard/create_edit_user.html', {'form': form, 'user':user})