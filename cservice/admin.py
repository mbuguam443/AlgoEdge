from django.contrib import admin
from .models import Service, ServiceRequest

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'price_from', 'is_featured', 'order']
    prepopulated_fields = {'slug': ['title']}

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'service', 'status', 'budget', 'deadline', 'created_at']
    list_filter = ['status']
