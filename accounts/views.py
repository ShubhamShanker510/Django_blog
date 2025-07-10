from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import registrationForm, loginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from blog.models import Post
from blog.forms import BlogForm1
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
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
    blog=Post.objects.all().order_by('-created_at')
    return render(request, 'dashboard/blog.html', {'blogs':blog})

@staff_member_required
def dashboard_user_view(request):
    user=User.objects.filter(is_superuser=False).order_by('-date_joined')
    return render(request, 'dashboard/user.html', {'users': user})

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
    

@staff_member_required
def dashboard_create_user(request):
    if request.method=="POST":
        form=registrationForm(request.POST)

        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "User created successfully")
            return redirect('/dashboard/users')
        
        else:
            messages.error(request, "Something went wrong")
    else:
        form=registrationForm()
    return render(request, 'dashboard/userform.html', {"form":form})

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
def edit_user(request, userid):
    user = User.objects.get(id=userid)

    if request.method == "POST":
        form = registrationForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)

            # ✅ Set password only if provided
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)

            user.save()
            messages.success(request, "User updated successfully")
            return redirect('/dashboard/users')
        else:
            messages.error(request, "Something went wrong")
    else:
        form = registrationForm(instance=user)

    return render(request, 'dashboard/userform.html', {'form': form, 'user': user})

@staff_member_required
def delete_user(request,userid):
    user=User.objects.get(id=userid)
    user.delete()
    messages.success(request, "User deleted successfully")
    return redirect('/dashboard/users')
        
@staff_member_required
def dashboard_categories_view(request):
    form=BlogForm1()
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
    
    
    categorychoices=form.fields['category'].choices
    authorchoices=form
    return render(request, 'dashboard/categories.html', {'blogs': blogs,'categorychoices': categorychoices, 'authorchoices': authorchoices, 'selected_category': category, 'selected_author': authorid})

