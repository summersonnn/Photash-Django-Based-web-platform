from django.urls import path
from .views import PhotoListAPIView, PhotoDetailAPIView, api_photo_delete

app_name = "photo_api"

urlpatterns = [
    path('<int:id>/', PhotoDetailAPIView.as_view(), name='detail'),
    path('<int:id>/delete/', api_photo_delete, name='delete'),
]