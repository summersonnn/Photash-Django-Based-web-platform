from django.shortcuts import render, HttpResponse, redirect
from user.forms import RegisterForm
from contest.models import Contest
from random import randint
from user.tokens import account_activation_token
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import Permission

def home_view(request):

    if not request.user.is_authenticated:
        count = Contest.objects.count()
        if count > 0:
            random_index = randint(0,count-1)
            random_contest = Contest.objects.all()[random_index]
        else:
            random_contest = None

        form = RegisterForm(data=request.POST or None)
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
                'photashtest@gmail.com',
                [user.email, ],
                fail_silently=False,
            )
            new_user = authenticate(username=user.username, password=password)
            login(request, new_user)

        context={
            'form': form,
            'random_contest': random_contest
        }
        return render(request, 'home/home.html', context)
    else:
        return render(request, 'home/timeline.html')

def catalogue_view(request):
    return render(request, 'home/catalogue.html')

@receiver(post_save, sender=User)
def add_default_permissions(sender, **kwargs):
    permission1 = Permission.objects.get(name='Can add new photos?')
    permission2 = Permission.objects.get(name='Can vote photos?')
    user = kwargs["instance"]
    if kwargs["created"]:
        user.user_permissions.add(permission1)
        user.user_permissions.add(permission2)



