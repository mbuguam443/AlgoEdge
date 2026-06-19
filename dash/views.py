from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from learn.models import Enrollment
from paygate.models import Order, Invoice
from pfarm.models import PropFirmChallenge
from copytrade.models import CopySubscription
from automate.models import StrategyProject
from alerts.models import Notification

class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'dash/home.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx['enrollments'] = Enrollment.objects.filter(user=user)[:5]
        ctx['orders'] = Order.objects.filter(user=user)[:5]
        ctx['invoices'] = Invoice.objects.filter(user=user)[:5]
        ctx['challenges'] = PropFirmChallenge.objects.filter(user=user)[:5]
        ctx['subscriptions'] = CopySubscription.objects.filter(user=user)[:5]
        ctx['projects'] = StrategyProject.objects.filter(user=user)[:5]
        ctx['notifications'] = Notification.objects.filter(user=user, is_read=False)[:5]
        return ctx

class DashboardProductsView(LoginRequiredMixin, TemplateView):
    template_name = 'dash/products.html'

class DashboardCoursesView(LoginRequiredMixin, TemplateView):
    template_name = 'dash/courses.html'

class DashboardDownloadsView(LoginRequiredMixin, TemplateView):
    template_name = 'dash/downloads.html'

class DashboardInvoicesView(LoginRequiredMixin, ListView):
    template_name = 'dash/invoices.html'
    context_object_name = 'invoices'
    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)

class DashboardProjectsView(LoginRequiredMixin, TemplateView):
    template_name = 'dash/projects.html'
