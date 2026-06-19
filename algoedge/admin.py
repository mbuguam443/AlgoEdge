from django.contrib import admin
from django.contrib.admin.models import LogEntry

admin.site.site_header = 'AlgoEdge Administration'
admin.site.site_title = 'AlgoEdge Admin Portal'
admin.site.index_title = 'Welcome to AlgoEdge Administration'
admin.site.site_url = '/'

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'object_repr', 'action_flag']
    list_filter = ['action_flag']
    date_hierarchy = 'action_time'
