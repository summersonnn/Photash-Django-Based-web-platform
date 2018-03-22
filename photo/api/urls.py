from django.urls import path
from .views import PhotoListAPIView, PhotoDetailAPIView, PhotoLikeAPIView, api_photo_delete, api_increase_seen_by_one

app_name = "photo_api"

urlpatterns = [
    path('<int:id>/', PhotoDetailAPIView.as_view(), name='detail'),
    path('<int:id>/delete/', api_photo_delete, name='delete'),
    path('<slug:slug>/index', PhotoListAPIView.as_view(), name="index_api"),
    path('like/', PhotoLikeAPIView.as_view(), name="like_api"),
    path('seen/', api_increase_seen_by_one, name='see'),
]