from django.urls import path
from . import views

app_name = 'copytrade'
urlpatterns = [
    path('', views.TraderListView.as_view(), name='traders'),
    path('<slug:slug>/', views.TraderDetailView.as_view(), name='trader_detail'),
    path('<int:pk>/subscribe/', views.SubscribeView.as_view(), name='subscribe'),
]
