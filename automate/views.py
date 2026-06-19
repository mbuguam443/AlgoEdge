from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import StrategyProject

class ProjectListView(LoginRequiredMixin, ListView):
    model = StrategyProject
    template_name = 'automate/projects.html'
    context_object_name = 'projects'
    def get_queryset(self):
        return StrategyProject.objects.filter(user=self.request.user)

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = StrategyProject
    fields = ['title', 'description', 'trading_rules', 'indicators', 'timeframes',
              'platforms', 'examples', 'screenshots', 'budget', 'deadline']
    template_name = 'automate/project_create.html'
    success_url = reverse_lazy('automate:projects')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = StrategyProject
    template_name = 'automate/project_detail.html'
    context_object_name = 'project'
    def get_queryset(self):
        return StrategyProject.objects.filter(user=self.request.user)
