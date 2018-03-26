from django.conf.urls import url
from django.urls import path
from .views import *

app_name = "home"

urlpatterns = [
    url(r'^catalogue/$', catalogue_view, name='catalogue'),
]