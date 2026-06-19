from django.urls import path
from . import views

app_name = 'cservice'
urlpatterns = [
    path('', views.ServiceListView.as_view(), name='services'),
    path('<slug:slug>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('request/new/', views.ServiceRequestCreateView.as_view(), name='service_request'),
]
