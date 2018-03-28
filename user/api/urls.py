from django.urls import path
from .views import ProfileDetailAPIView, UpdatePreferedTags, read_notification, NotificationsAPIView

app_name = 'user_api'

urlpatterns = [
    path('profile/<int:pk>', ProfileDetailAPIView.as_view(), name='profile'),
    path('update-prefered-tags/', UpdatePreferedTags.as_view(), name='update_prefered_tags'),
    path('notification/', NotificationsAPIView.as_view(), name='notification'),
    path('notification/read/<int:id>', read_notification, name='read_notification'),

]