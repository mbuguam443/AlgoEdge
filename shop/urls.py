from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='products'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
