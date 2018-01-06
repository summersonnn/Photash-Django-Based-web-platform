from django.conf.urls import url
from .views import *

app_name = "photo"

urlpatterns = [

    url(r'^(?P<contestslug>[\w-]+)/index/$', photo_index, name="index"),
    url(r'^(?P<id>\d+)/$', photo_detail, name='detail'),
    url(r'^(?P<contestslug>[\w-]+)/create/$', photo_create, name="create"),
    url(r'^(?P<id>\d+)/delete/$', photo_delete),


]