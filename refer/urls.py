from django.urls import path
from . import views

app_name = 'refer'
urlpatterns = [
    path('', views.AffiliateDashboardView.as_view(), name='dashboard'),
]
