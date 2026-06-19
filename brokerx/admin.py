from django.contrib import admin
from .models import BrokerVerification, AffiliateReferral, Payout

@admin.register(BrokerVerification)
class BrokerVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'broker_name', 'account_number', 'status', 'created_at']
    list_filter = ['status']

@admin.register(AffiliateReferral)
class AffiliateReferralAdmin(admin.ModelAdmin):
    list_display = ['user', 'referred_email', 'broker_verified', 'commission_earned']

@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'method', 'status', 'created_at']
