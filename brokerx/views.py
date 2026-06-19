from django.views.generic import ListView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import BrokerVerification, AffiliateReferral

class BrokerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'brokerx/dashboard.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['verifications'] = BrokerVerification.objects.filter(user=self.request.user)
        ctx['referrals'] = AffiliateReferral.objects.filter(user=self.request.user)
        return ctx

class VerificationCreateView(LoginRequiredMixin, CreateView):
    model = BrokerVerification
    fields = ['broker_name', 'account_number', 'account_type', 'account_size', 'screenshot']
    template_name = 'brokerx/verify.html'
    success_url = reverse_lazy('brokerx:dashboard')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
