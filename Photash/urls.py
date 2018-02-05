from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from photo.api import views as api_views
from home.views import home_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    url(r'^$', home_view, name = 'home'),

    url(r'^photo/', include('photo.urls', namespace="photo")),

    url(r'^contest/', include('contest.urls')),

    url(r'^user/', include('user.urls')),

    url(r'^admin/', admin.site.urls),

    url(r'^ratings/', include('star_ratings.urls', namespace = 'ratings')),

    url(r'^api/report-photo/', include('reportedPhotos.api.urls', namespace='reportedPhotos_api')),

    path('api/<slug:slug>/index/', api_views.PhotoListAPIView.as_view(), name="index_api"),

    path('api/user/', include('user.api.urls', namespace='user_api')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)