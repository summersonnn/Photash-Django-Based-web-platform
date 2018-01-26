from django.conf.urls import url, include
from django.contrib import admin
from home.views import home_view, learnmore_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    url(r'^$', home_view, name = 'home'),

    url(r'^learnmore/$', learnmore_view, name = 'learnmore'),

    url(r'^photo/', include('photo.urls', namespace="photo")),

    url(r'^contest/', include('contest.urls')),

    url(r'^user/', include('user.urls')),

    url(r'^admin/', admin.site.urls),

    url(r'^ratings/', include('star_ratings.urls', namespace = 'ratings')),

    url(r'^api/report-photo/', include('reportedPhotos.api.urls', namespace='reportedPhotos_api')),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)