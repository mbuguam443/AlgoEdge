from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AffiliateAccount
from brokerx.models import AffiliateReferral

class AffiliateDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'refer/dashboard.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        try:
            ctx['affiliate'] = AffiliateAccount.objects.get(user=self.request.user)
        except AffiliateAccount.DoesNotExist:
            pass
        ctx['referrals'] = AffiliateReferral.objects.filter(user=self.request.user)
        return ctx
