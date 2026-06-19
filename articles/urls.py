from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog'),
    path('<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
]
