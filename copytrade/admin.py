from django.contrib import admin
from .models import MasterTrader, CopySubscription, PerformanceHistory, Signal

@admin.register(MasterTrader)
class MasterTraderAdmin(admin.ModelAdmin):
    list_display = ['name', 'roi', 'win_rate', 'max_drawdown', 'followers', 'is_active']
    list_filter = ['is_active', 'is_verified', 'risk_level']
    prepopulated_fields = {'slug': ['name']}

@admin.register(CopySubscription)
class CopySubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'trader', 'amount', 'is_active', 'started_at']

@admin.register(PerformanceHistory)
class PerformanceHistoryAdmin(admin.ModelAdmin):
    list_display = ['trader', 'date', 'equity', 'daily_pnl', 'drawdown']

@admin.register(Signal)
class SignalAdmin(admin.ModelAdmin):
    list_display = ['trader', 'instrument', 'direction', 'entry_price', 'status', 'pnl']
