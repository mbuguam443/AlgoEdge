from django.contrib import admin
from .models import StrategyProject, ProjectMilestone, ProjectMessage

@admin.register(StrategyProject)
class StrategyProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'progress', 'budget', 'created_at']
    list_filter = ['status']

@admin.register(ProjectMilestone)
class ProjectMilestoneAdmin(admin.ModelAdmin):
    list_display = ['project', 'title', 'due_date', 'is_completed']

@admin.register(ProjectMessage)
class ProjectMessageAdmin(admin.ModelAdmin):
    list_display = ['project', 'user', 'is_admin', 'created_at']
