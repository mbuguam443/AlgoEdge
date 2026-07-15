from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View, FormView, DetailView
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AdminPasswordChangeForm
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Sum, Q, Avg
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.template.loader import render_to_string
from datetime import timedelta
from .mixins import StaffRequiredMixin

User = get_user_model()

class DashboardView(StaffRequiredMixin, TemplateView):
    template_name = 'cadmin/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        month_start = today_start.replace(day=1)

        try:
            from django.contrib.auth.models import User
            from shop.models import Product, Order
            from learn.models import Course, Enrollment
            from pfarm.models import PropFirm, Challenge
            from copytrade.models import Trader, Signal
            from brokerx.models import EALicense
            from cservice.models import Service
            from refer.models import Referral
            from automate.models import Project
        except ImportError:
            Product = Order = Course = Enrollment = None
            PropFirm = Challenge = Trader = Signal = EALicense = None
            Service = Referral = Project = None

        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        new_users_today = User.objects.filter(date_joined__gte=today_start).count()
        total_orders = Order.objects.count() if Order else 0
        orders_today = Order.objects.filter(created_at__gte=today_start).count() if Order else 0
        total_courses = Course.objects.count() if Course else 0
        total_enrollments = Enrollment.objects.count() if Enrollment else 0
        total_products = Product.objects.count() if Product else 0
        total_signals = Signal.objects.count() if Signal else 0
        total_challenges = Challenge.objects.count() if Challenge else 0
        total_projects = Project.objects.count() if Project else 0
        total_services = Service.objects.count() if Service else 0
        active_subscriptions = Enrollment.objects.count() if Enrollment else 0

        recent_logs = LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:10]

        users_chart = []
        for i in range(7):
            day = now - timedelta(days=i)
            day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
            users_chart.append(User.objects.filter(date_joined__gte=day_start, date_joined__lt=day_start + timedelta(days=1)).count())
        users_chart.reverse()

        orders_chart = []
        for i in range(7):
            day = now - timedelta(days=i)
            day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
            orders_chart.append(Order.objects.filter(created_at__gte=day_start, created_at__lt=day_start + timedelta(days=1)).count() if Order else 0)
        orders_chart.reverse()

        ctx.update({
            'total_users': total_users, 'active_users': active_users,
            'new_users_today': new_users_today,
            'total_orders': total_orders, 'orders_today': orders_today,
            'total_courses': total_courses, 'total_enrollments': total_enrollments,
            'total_products': total_products, 'total_signals': total_signals,
            'total_challenges': total_challenges, 'total_projects': total_projects,
            'total_services': total_services, 'active_subscriptions': active_subscriptions,
            'recent_logs': recent_logs,
            'users_chart': users_chart,
            'orders_chart': orders_chart,
            'page_title': 'Dashboard',
            'app_label': 'dashboard',
        })
        return ctx

class ModelListView(StaffRequiredMixin, ListView):
    template_name = 'cadmin/model_list.html'
    paginate_by = 25

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        meta = self.model._meta
        ctx.update({
            'page_title': f'Manage {meta.verbose_name_plural.title()}',
            'app_label': meta.app_label,
            'model_name': meta.model_name,
            'verbose_name': meta.verbose_name,
            'verbose_name_plural': meta.verbose_name_plural,
            'fields': [f for f in meta.fields if f.name != 'id'],
            'add_url': reverse(f'cadmin:{meta.model_name}_create'),
            'has_add': True,
        })
        return ctx

class ModelCreateView(StaffRequiredMixin, CreateView):
    template_name = 'cadmin/model_form.html'

    def get_form(self, form_class=None):
        from django.forms import modelform_factory
        form_class = modelform_factory(self.model, fields='__all__')
        return form_class(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        meta = self.model._meta
        ctx.update({
            'page_title': f'New {meta.verbose_name.title()}',
            'app_label': meta.app_label,
            'model_name': meta.model_name,
            'verbose_name': meta.verbose_name,
            'is_create': True,
        })
        return ctx

    def form_valid(self, form):
        messages.success(self.request, f'{self.model._meta.verbose_name.title()} created successfully.')
        return super().form_valid(form)

class ModelUpdateView(StaffRequiredMixin, UpdateView):
    template_name = 'cadmin/model_form.html'

    def get_form(self, form_class=None):
        from django.forms import modelform_factory
        form_class = modelform_factory(self.model, fields='__all__')
        return form_class(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        meta = self.model._meta
        ctx.update({
            'page_title': f'Edit {meta.verbose_name.title()}',
            'app_label': meta.app_label,
            'model_name': meta.model_name,
            'verbose_name': meta.verbose_name,
            'is_create': False,
        })
        return ctx

    def form_valid(self, form):
        messages.success(self.request, f'{self.model._meta.verbose_name.title()} updated successfully.')
        return super().form_valid(form)

class ModelDeleteView(StaffRequiredMixin, DeleteView):
    template_name = 'cadmin/model_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, f'{self.model._meta.verbose_name.title()} deleted successfully.')
        return reverse(f'cadmin:{self.model._meta.model_name}_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        meta = self.model._meta
        ctx.update({
            'page_title': f'Delete {meta.verbose_name.title()}',
            'app_label': meta.app_label,
            'model_name': meta.model_name,
            'verbose_name': meta.verbose_name,
        })
        return ctx

class UserListView(StaffRequiredMixin, ListView):
    template_name = 'cadmin/model_list.html'
    model = User
    paginate_by = 25

    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'page_title': 'Manage Users',
            'app_label': 'auth',
            'model_name': 'users',
            'verbose_name': 'User',
            'verbose_name_plural': 'Users',
            'fields': [f for f in User._meta.fields if f.name not in ('id', 'password', 'last_login')],
            'add_url': reverse('cadmin:users_create'),
            'has_add': True,
        })
        return ctx

class UserCreateView(StaffRequiredMixin, CreateView):
    template_name = 'cadmin/model_form.html'
    model = User
    form_class = UserCreationForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({'page_title': 'New User', 'app_label': 'auth', 'model_name': 'users', 'verbose_name': 'User', 'is_create': True})
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'User created successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('cadmin:users_list')

class UserUpdateView(StaffRequiredMixin, UpdateView):
    template_name = 'cadmin/user_form.html'
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({'page_title': f'Edit User: {self.object.username}', 'app_label': 'auth', 'model_name': 'users', 'verbose_name': 'User', 'is_create': False})
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'User updated successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('cadmin:users_list')

class UserPasswordView(StaffRequiredMixin, FormView):
    template_name = 'cadmin/user_password.html'
    form_class = AdminPasswordChangeForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = get_object_or_404(User, pk=self.kwargs['pk'])
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        ctx.update({'page_title': f'Change Password: {user.username}', 'app_label': 'auth', 'model_name': 'users', 'verbose_name': 'User', 'password_user': user})
        return ctx

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Password changed successfully.')
        return redirect('cadmin:users_list')

class UserDeleteView(StaffRequiredMixin, DeleteView):
    template_name = 'cadmin/model_confirm_delete.html'
    model = User

    def get_success_url(self):
        messages.success(self.request, 'User deleted successfully.')
        return reverse('cadmin:users_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({'page_title': f'Delete User: {self.object.username}', 'app_label': 'auth', 'model_name': 'users', 'verbose_name': 'User'})
        return ctx
