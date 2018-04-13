from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegisterForm, ProfileForm
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.db import transaction
from django.urls import reverse
from django.contrib import messages
from .models import Profile

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if(user.is_active == False):
            return render(request, 'accounts/you_are_banned.html')
        else:
            login(request, user)
        username = User.objects.get(username=request.user)
        url = reverse('home')
        return HttpResponseRedirect(url)
    return render(request, 'accounts/form.html', {'form': form, 'title': 'Login'})


'''def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password1')
        user.set_password(password)
        user.save()
        # mail verification
        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        send_mail(
            'Please confirm your photash account',
            'Click the link belox \n http://127.0.0.1:8000/user/activate/{}/{}'.format(uid, token),
            'altunerism@gmail.com',
            [user.email, ],
            fail_silently=False,
        )
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect('home')
    return render(request, 'accounts/form.html', {'form': form, 'title': 'Sign up'})'''


@login_required
def activate_account(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64).decode()
    user = get_object_or_404(User, id=uid)

    if request.user != user or not account_activation_token.check_token(user, token):
        return HttpResponseRedirect('/')

    profile = user.profile
    profile.email_verified = True
    profile.save()
    return HttpResponseRedirect('/')


def logout_view(request):
    logout(request)
    return redirect('home')


# --------------------------------------------------------------------------------------------
def profile_view(request):
    return render(request, 'user/profile.html')

def myprofileview(request, username):
    profile = Profile.objects.get(user = request.user)
    return render(request,'user/profile.html',{'profile':profile})


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

