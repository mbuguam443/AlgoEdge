from django.contrib import admin
from .models import UserProfile, EAWallet

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'country', 'is_verified', 'broker_verified', 'wallet_balance', 'created_at']
    list_filter = ['is_verified', 'broker_verified', 'country']
    search_fields = ['user__username', 'user__email', 'phone']

@admin.register(EAWallet)
class EAWalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'license_key', 'mt5_account', 'is_active', 'expires_at']
    list_filter = ['is_active']
    search_fields = ['user__username', 'product', 'license_key']
