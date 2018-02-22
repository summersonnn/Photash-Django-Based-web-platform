from django.shortcuts import render, HttpResponse
from user.forms import RegisterForm

def home_view(request):
    return render(request, 'home/home.html', {'register_form': RegisterForm})

def feed_view(request):
    return render(request, 'home/feed.html')



