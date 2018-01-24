from django.conf.urls import url
from django.urls import path
from .views import *

app_name = "user"

urlpatterns = [

    url(r'^login/$', login_view, name = "login"),
    url(r'^register/$', register_view, name = "register"),
    url(r'^logout/$', logout_view, name = "logout"),
    url(r'^profile/$', profile_view, name = "profile"),
    url(r'^editprofile/$', update_profile, name = "updateprofile"),
    #url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})', activate_account, name='activate_account'),
    path('activate/<uidb64>/<token>/', activate_account, name="activate_account"),


]