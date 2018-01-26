from django.conf.urls import url
from django.urls import path
from .views import *
from photo.api import views as api_views

app_name = "photo"

urlpatterns = [

    url(r'^(?P<contestslug>[\w-]+)/index/$', photo_index, name="index"),
    path('api/<slug:contest>/index/', api_views.PhotoListAPIView.as_view(), name="index_api"),
    path('get-rating/<int:id>/', get_photo_rating, name="get_photo_rating"),
    url(r'^(?P<id>\d+)/$', photo_detail, name='detail'),
    url(r'^(?P<contestslug>[\w-]+)/create/$', photo_create, name="create"),
    url(r'^(?P<id>\d+)/delete/$', photo_delete),


]