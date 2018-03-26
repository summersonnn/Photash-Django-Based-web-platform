from django.shortcuts import render, HttpResponse, redirect
from user.forms import RegisterForm
from contest.models import Contest
from random import randint
from user.tokens import account_activation_token
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import send_mail

def home_view(request):
    count = Contest.objects.count()
    if count > 0:
        random_index = randint(0,count-1)
        random_contest = Contest.objects.all()[random_index]
    else:
        random_contest = None
    random_contest=None

    form = RegisterForm(data=request.POST or None)
    if form.is_valid():
        print("form is valid babe")
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
    else:
        print("form is NOT valid babe")

    context={
        'form': form,
        'random_contest': random_contest
    }
    return render(request, 'home/home.html', context)

def catalogue_view(request):
    return render(request, 'home/catalogue.html')


