
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Permission
from django.urls import reverse
from .forms import SignUpForm, LoginForm, EditProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .models import User, Profile

from django.contrib import messages
def signup(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if request.POST.get("is_producer", ""):
                user.is_staff = True
                user.save()
            login(request, user)
            messages.success(request, "Congratulations, you are now a registered user!")
            return redirect('core:home')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

def log_in(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user: 
                login(request, user)
                return redirect('core:home')
            else:
                messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect(reverse('users:login'))

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'users/profile.html', {'profile': profile, 'user': user})

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.user.username, request.POST, request.FILES)
        if form.is_valid():
            about_me = form.cleaned_data["about_me"]
            username = form.cleaned_data["username"]
            image = form.cleaned_data["image"]

            user = User.objects.get(id=request.user.id)
            profile = Profile.objects.get(user=user)
            user.username = username
            user.save()
            profile.about_me = about_me
            if image:
                profile.image = image
            profile.save()
            return redirect("users:profile", username=user.username)
    else:
        form = EditProfileForm(request.user.username)
    return render(request, "users/edit_profile.html", {'form': form})