from django import template
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count

register = template.Library()

@register.simple_tag
def get_admin_stats():
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        from shop.models import Order
        return {
            'total_users': User.objects.count(),
            'total_orders': Order.objects.count(),
        }
    except:
        return {}

@register.filter
def field_value(obj, field_name):
    return getattr(obj, field_name, '')

@register.filter
def verbose_name(obj):
    return obj._meta.verbose_name.title()

@register.filter
def model_name(obj):
    return obj._meta.model_name

@register.filter
def app_label(obj):
    return obj._meta.app_label

@register.simple_tag
def get_content_types():
    return ContentType.objects.annotate(total=Count('logentry')).filter(total__gt=0)
