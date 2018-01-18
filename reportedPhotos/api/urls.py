from django.conf.urls import url
from .views import ReportPhotoAPIView

app_name = 'reportedPhotos_api'

urlpatterns = [
    url(r'^(?P<id>[0-9]+)/$', ReportPhotoAPIView.as_view(), name="report_photo"),
]