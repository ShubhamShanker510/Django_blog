from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import registrationForm, loginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from blog.models import Post
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



class AdminLoginRedirectView(LoginView):
    template_name = 'admin/login.html'  # Use Django’s default admin template
    redirect_authenticated_user = True  # Optional, if user is already logged in

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('custom_admin_dashboard')  # Send to /dashboard/
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
    user=User.objects.all().order_by('-date_joined')
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