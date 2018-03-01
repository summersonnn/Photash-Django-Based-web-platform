from django.urls import path
from .views import ProfileDetailAPIView, UpdatePreferedTags

app_name = 'user_api'

urlpatterns = [
    path('profile/<int:pk>', ProfileDetailAPIView.as_view(), name='profile'),
    path('update-prefered-tags/', UpdatePreferedTags.as_view(), name='update_prefered_tags')
]