from django.urls import path
from . import views

app_name = 'automate'
urlpatterns = [
    path('', views.ProjectListView.as_view(), name='projects'),
    path('new/', views.ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
]
