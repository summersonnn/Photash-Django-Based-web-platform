from django.conf.urls import url
from .views import *

app_name = "user"

urlpatterns = [

    url(r'^login/$', login_view, name = "login"),
    url(r'^register/$', register_view, name = "register"),
    url(r'^logout/$', logout_view, name = "logout"),
    url(r'^profile/$', profile_view, name = "profile"),
    url(r'^editprofile/$', update_profile, name = "updateprofile"),


]