from django.conf.urls import url
from .views import *

app_name = "contest"

urlpatterns = [

    url(r'^(?P<slug>[\w-]+)/photos/$', contest_photopool, name="photopool"),
    url(r'^(?P<slug>[\w-]+)/upload/$', photo_upload, name="photo_upload"),
    url(r'^index/$', contest_index, name="index"),
    url(r'^(?P<slug>[\w-]+)/$', contest_detail, name='detail'),  # Aslında template içinde bu url çağırılmıyor. Çünkü template içinde url ismini vererek çağırırken parametre vermeyi başaramadım. eğer sonra düzeltirsem diye, url'e de slug koydum.
    # url(r'^create/$', photo_create), CONTEST OLUŞTURMAK ŞİMDİLİK USER TARAFINDAN YAPILAMAYACAGI İÇİN NE FORM NE DE VİEW YAZACAĞIM (SANIRIM)
    url(r'^(?P<id>\d+)/delete/$', contest_delete),
    url(r'^(?P<slug>[\w-]+)/rankings/$', contest_rankings, name='rankings'),

]