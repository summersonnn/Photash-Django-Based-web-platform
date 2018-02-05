from django.urls import path
from .views import ProfileDetailAPIView

app_name = 'user_api'

urlpatterns = [
    path('profile/<int:pk>', ProfileDetailAPIView.as_view(), name='profile'),
]