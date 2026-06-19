from django.urls import path
from . import views

app_name = 'pfarm'
urlpatterns = [
    path('', views.FirmListView.as_view(), name='firms'),
    path('challenges/', views.ChallengeListView.as_view(), name='challenges'),
    path('challenges/new/', views.ChallengeCreateView.as_view(), name='challenge_create'),
    path('challenges/<int:pk>/', views.ChallengeDetailView.as_view(), name='challenge_detail'),
]
