import os

BASE = r"C:\Users\mbugu\OneDrive\Desktop\OpenCode\Trading Services website"

apps_config = {
    'home': {
        'forms': """
from django import forms
from .models import ContactMessage, Newsletter

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your message...', 'rows': 5}),
        }

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        }
""",
        'urls': """
from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('pricing/', views.PricingView.as_view(), name='pricing'),
    path('newsletter/', views.newsletter_subscribe, name='newsletter'),
]
""",
        'views': """
from django.views.generic import TemplateView, FormView
from django.http import JsonResponse
from django.shortcuts import render
from .models import Testimonial, FAQ, ContactMessage
from .forms import ContactForm, NewsletterForm
from articles.models import Newsletter

class IndexView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['testimonials'] = Testimonial.objects.filter(is_featured=True)
        ctx['faqs'] = FAQ.objects.filter(is_published=True)[:6]
        return ctx

class AboutView(TemplateView):
    template_name = 'home/about.html'

class ContactView(FormView):
    template_name = 'home/contact.html'
    form_class = ContactForm
    success_url = '/contact/?success=1'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class FAQView(TemplateView):
    template_name = 'home/faq.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['faqs'] = FAQ.objects.filter(is_published=True)
        return ctx

class PricingView(TemplateView):
    template_name = 'home/pricing.html'

def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            Newsletter.objects.get_or_create(email=email)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
""",
    },
    'userauth': {
        'forms': """
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'phone', 'country', 'bio', 'mt4_account', 'mt5_account']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'mt4_account': forms.TextInput(attrs={'class': 'form-control'}),
            'mt5_account': forms.TextInput(attrs={'class': 'form-control'}),
        }
""",
        'urls': """
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'userauth'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home:index'), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='userauth/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='userauth/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='userauth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='userauth/password_reset_complete.html'), name='password_reset_complete'),
]
""",
        'views': """
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import RegistrationForm, LoginForm, ProfileForm
from refer.models import AffiliateAccount
import uuid

class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'userauth/register.html'
    success_url = reverse_lazy('login')

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
""",
    },
    'learn': {
        'forms': "",
        'urls': """
from django.urls import path
from . import views

app_name = 'learn'
urlpatterns = [
    path('', views.CourseListView.as_view(), name='courses'),
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('<slug:course_slug>/lesson/<slug:slug>/', views.LessonDetailView.as_view(), name='lesson_detail'),
]
""",
        'views': """
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Course, Lesson, Enrollment, LessonProgress

class CourseListView(ListView):
    model = Course
    template_name = 'learn/courses.html'
    context_object_name = 'courses'
    paginate_by = 12

    def get_queryset(self):
        qs = Course.objects.filter(is_published=True)
        cat = self.request.GET.get('category')
        level = self.request.GET.get('level')
        if cat: qs = qs.filter(category__slug=cat)
        if level: qs = qs.filter(level=level)
        return qs

class CourseDetailView(DetailView):
    model = Course
    template_name = 'learn/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        course = self.get_object()
        if self.request.user.is_authenticated:
            ctx['is_enrolled'] = Enrollment.objects.filter(user=self.request.user, course=course).exists()
        return ctx

class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'learn/lesson.html'
    context_object_name = 'lesson'

    def get_object(self):
        course = get_object_or_404(Course, slug=self.kwargs['course_slug'])
        return get_object_or_404(Lesson, course=course, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        lesson = self.get_object()
        ctx['course'] = lesson.course
        enrolled = Enrollment.objects.filter(user=self.request.user, course=lesson.course).exists()
        if not enrolled and not lesson.is_free:
            ctx['locked'] = True
        return ctx
""",
    },
}

def write_app_files():
    for app_name, config in apps_config.items():
        app_dir = os.path.join(BASE, app_name)
        for ftype, content in config.items():
            filepath = os.path.join(app_dir, f'{ftype}.py')
            if content:
                # Check if file already exists and has content we don't want to overwrite
                existing = ""
                if os.path.exists(filepath):
                    with open(filepath) as f:
                        existing = f.read()
                if 'from django' in existing and 'import' in existing:
                    # File has real content, append to existing header
                    final = existing.rstrip() + '\n\n' + content
                else:
                    final = content
                with open(filepath, 'w') as f:
                    f.write(final)
                print(f"Written: {filepath}")

if __name__ == '__main__':
    write_app_files()
