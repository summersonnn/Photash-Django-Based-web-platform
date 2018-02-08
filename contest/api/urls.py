from django.urls import path
from .views import ContestListAPIView, ContestDetailAPIView

app_name = 'contest_api'

urlpatterns = [
    path('index', ContestListAPIView.as_view(), name='index'),
    path('<slug:slug>/', ContestDetailAPIView.as_view(), name='detail'),
]
