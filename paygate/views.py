from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Invoice, Payment, Order

class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'paygate/invoices.html'
    context_object_name = 'invoices'
    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'paygate/orders.html'
    context_object_name = 'orders'
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class CheckoutView(TemplateView):
    template_name = 'paygate/checkout.html'
