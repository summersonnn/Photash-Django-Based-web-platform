from django.urls import path
from .views import PhotoListAPIView

app_name = "photo_api"

urlpatterns = [
    path('<slug:contestslug>/index/', PhotoListAPIView, name="index"),
]