from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import PropFirm, PropFirmChallenge

class FirmListView(ListView):
    model = PropFirm
    template_name = 'pfarm/firms.html'
    context_object_name = 'firms'
    queryset = PropFirm.objects.filter(is_active=True)

class ChallengeListView(LoginRequiredMixin, ListView):
    model = PropFirmChallenge
    template_name = 'pfarm/challenges.html'
    context_object_name = 'challenges'
    def get_queryset(self):
        return PropFirmChallenge.objects.filter(user=self.request.user)

class ChallengeCreateView(LoginRequiredMixin, CreateView):
    model = PropFirmChallenge
    fields = ['firm', 'account_number', 'account_size', 'challenge_type', 'profit_target',
              'daily_drawdown_limit', 'max_drawdown_limit', 'total_days', 'trading_platform']
    template_name = 'pfarm/challenge_create.html'
    success_url = reverse_lazy('pfarm:challenges')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['firms'] = PropFirm.objects.filter(is_active=True)
        return ctx
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ChallengeDetailView(LoginRequiredMixin, DetailView):
    model = PropFirmChallenge
    template_name = 'pfarm/challenge_detail.html'
    context_object_name = 'challenge'
