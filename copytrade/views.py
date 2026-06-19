from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import MasterTrader, CopySubscription

class TraderListView(ListView):
    model = MasterTrader
    template_name = 'copytrade/traders.html'
    context_object_name = 'traders'
    queryset = MasterTrader.objects.filter(is_active=True)

class TraderDetailView(DetailView):
    model = MasterTrader
    template_name = 'copytrade/trader_detail.html'
    context_object_name = 'trader'

class SubscribeView(LoginRequiredMixin, CreateView):
    model = CopySubscription
    fields = ['amount']
    template_name = 'copytrade/subscribe.html'
    success_url = reverse_lazy('dashboard:home')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['trader'] = MasterTrader.objects.get(pk=self.kwargs['pk'])
        return ctx

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.trader_id = self.kwargs['pk']
        return super().form_valid(form)
