from django.urls import path
from . import views

app_name = 'paygate'
urlpatterns = [
    path('invoices/', views.InvoiceListView.as_view(), name='invoices'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
]
