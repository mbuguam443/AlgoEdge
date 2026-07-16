from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .models import UserProfile
from .forms import RegistrationForm, LoginForm, ProfileForm
from refer.models import AffiliateAccount
import uuid

class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'userauth/register.html'
    success_url = reverse_lazy('userauth:login')

    def form_valid(self, form):
        user = form.save()
        code = uuid.uuid4().hex[:8]
        AffiliateAccount.objects.create(user=user, code=code)
        ref = self.request.GET.get('ref')
        if ref:
            try:
                aff = AffiliateAccount.objects.get(code=ref)
                user.profile.referred_by = aff.user.profile
                user.profile.save()
            except AffiliateAccount.DoesNotExist:
                pass
        return super().form_valid(form)

class LoginView(AuthLoginView):
    form_class = LoginForm
    template_name = 'userauth/login.html'

    def get_success_url(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return reverse('cadmin:dashboard')
        return reverse('dashboard:home')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'userauth/profile.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['profile'] = self.request.user.profile
        return ctx

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = ProfileForm
    template_name = 'userauth/profile_edit.html'
    success_url = reverse_lazy('userauth:profile')
    def get_object(self):
        return self.request.user.profile
