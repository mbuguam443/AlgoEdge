from django.contrib import admin
from .models import AffiliateAccount

@admin.register(AffiliateAccount)
class AffiliateAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'total_earnings', 'total_referrals', 'is_active']
