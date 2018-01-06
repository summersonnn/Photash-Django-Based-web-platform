from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
#from .models import Profile

# Create your views here.
def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username = username, password = password)
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/form.html', {'form': form, 'title': 'Login'})

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit = False)
        password = form.cleaned_data.get('password1')
        user.set_password(password)
        user.save()
        new_user = authenticate(username = user.username, password = password)
        login(request, new_user)
        return redirect('home')
    return render(request, 'accounts/form.html', {'form': form, 'title': 'Sign up'})

def logout_view(request):
    logout(request)
    return redirect('home')

#--------------------------------------------------------------------------------------------
def profile_view(request):
    return render(request, 'user/profile.html')

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = RegisterForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'user/editprofile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

