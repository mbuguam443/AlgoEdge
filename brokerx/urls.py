from django.urls import path
from . import views

app_name = 'brokerx'
urlpatterns = [
    path('', views.BrokerDashboardView.as_view(), name='dashboard'),
    path('verify/', views.VerificationCreateView.as_view(), name='verify'),
]
