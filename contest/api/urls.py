from django.urls import path
from .views import ContestListAPIView, ContestDetailAPIView, VotersListAPIView, FeedAPIView, AskForTags, ContestRankingAPIView

app_name = 'contest_api'

urlpatterns = [
    path('index/', ContestListAPIView.as_view(), name='index'),
    path('<slug:slug>/detail/', ContestDetailAPIView.as_view(), name='detail'),
    path('<slug:slug>/voters/', VotersListAPIView.as_view(), name='voters'),
    path('<slug:slug>/rankings/', ContestRankingAPIView.as_view(), name='rankings'),
    path('timeline/', FeedAPIView.as_view(), name='timeline'),
    path('ask-for-tags/', AskForTags.as_view(), name='ask_for_tags'),
]
