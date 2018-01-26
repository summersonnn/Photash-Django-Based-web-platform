from django.conf.urls import url
from django.urls import path
from .views import *
from photo.api import views as api_views

app_name = "photo"

urlpatterns = [

    #url(r'^(?P<contestslug>[\w-]+)/index/$', photo_index, name="index"),
    path('<slug:contestslug>/index/', api_views.PhotoListAPIView.as_view(), name="index"),
    url(r'^(?P<id>\d+)/$', photo_detail, name='detail'),
    url(r'^(?P<contestslug>[\w-]+)/create/$', photo_create, name="create"),
    url(r'^(?P<id>\d+)/delete/$', photo_delete),


]