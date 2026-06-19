from django.urls import path
from . import views

app_name = 'metrics'
urlpatterns = [
    path('health/', views.health_check, name='health'),
]
