from django.urls import path
from .views import ContestListAPIView, ContestDetailAPIView, VotersListAPIView, FeedAPIView

app_name = 'contest_api'

urlpatterns = [
    path('index/', ContestListAPIView.as_view(), name='index'),
    path('<slug:slug>/', ContestDetailAPIView.as_view(), name='detail'),
    path('<slug:slug>/voters/', VotersListAPIView.as_view(), name='voters'),
    path('timeline', FeedAPIView.as_view(), name='timeline'),
]
