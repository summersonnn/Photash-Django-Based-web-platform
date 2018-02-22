from django.conf.urls import url
from django.urls import path
from .views import *

app_name = "home"

urlpatterns = [
    url(r'^feed/$', feed_view, name='feed'),
]