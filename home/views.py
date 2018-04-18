from django.shortcuts import render, HttpResponse, redirect
from user.forms import RegisterForm
from contest.models import Contest
from random import randint
from user.tokens import account_activation_token
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import send_mail
import geoip2.webservice
from django.contrib import messages

def home_view(request):

    if not request.user.is_authenticated:

        #Getting a random contest to be used in steps section
        count = Contest.objects.count()
        if count > 0:
            random_index = randint(0,count-1)
            random_contest = Contest.objects.all()[random_index]
        else:
            random_contest = None

        #Sign up form
        form = RegisterForm(data=request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password1')
            user.set_password(password)
            user.save()
            messages.success(request, "Thank you for joining our community. Explore the best photos on Photash!", extra_tags="alert-success")

            #setting language by the IP
            client = geoip2.webservice.Client(132292, '9uNrE6xTWGHX')
            ip = get_ip(request)
            response = client.city('176.240.19.15')  # Uzak server'a yüklendiğinde burdaki harcoded ip yerine ip yazılacak. Şu an yazılınca 127.0.0.1 hata çıkartıyor o yüzden yazılmadı
            if (response.country.iso_code == "TR"):
                user.profile.languagePreference ="tr"
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

        # Guestler için session kontrolü
        # Session'da language belirlenmemiş ise önce belirleyelim
        if "language" not in request.session:
            set_session_for_language_according_to_IP(request)

        if (request.session['language'] == "tr"):
            return render(request, 'home/home-tr.html', context)
        else:
            return render(request, 'home/home.html', context)
    else:
        return render(request, 'home/timeline.html')

def catalogue_view(request):
    if request.user.is_authenticated:
        if request.user.profile.languagePreference == "en":
            return render(request, 'home/catalogue.html')
        else:
            return render(request, 'home/catalogue-tr.html')

    #Guestler için session kontrolü
    # Session'da language belirlenmemiş ise önce belirleyelim
    if "language" not in request.session:
        set_session_for_language_according_to_IP(request)

    if (request.session['language'] == "tr"):
        return render(request, 'home/catalogue-tr.html')
    else:
        return render(request, 'home/catalogue.html')


def get_ip(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""
    return ip

def set_session_for_language_according_to_IP(request):
    # Setting the language according to the IP of the guest
    client = geoip2.webservice.Client(132292, '9uNrE6xTWGHX')
    ip = get_ip(request)
    response = client.city('195.175.89.86')  # Uzak server'a yüklendiğinde burdaki harcoded ip yerine ip yazılacak. Şu an yazılınca 127.0.0.1 hata çıkartıyor o yüzden yazılmadı
    if (response.country.iso_code == "TR"):
        request.session['language'] = "tr"
    else:
        request.session['language'] = "en"
    return None





