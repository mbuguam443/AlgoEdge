from django.contrib import admin
from .models import PropFirm, PropFirmChallenge, DailyEquity, TradeRecord

@admin.register(PropFirm)
class PropFirmAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'is_active']

@admin.register(PropFirmChallenge)
class PropFirmChallengeAdmin(admin.ModelAdmin):
    list_display = ['user', 'firm', 'account_size', 'status', 'current_profit', 'days_remaining']
    list_filter = ['status', 'firm']

@admin.register(DailyEquity)
class DailyEquityAdmin(admin.ModelAdmin):
    list_display = ['challenge', 'date', 'equity', 'daily_pnl', 'drawdown']

@admin.register(TradeRecord)
class TradeRecordAdmin(admin.ModelAdmin):
    list_display = ['challenge', 'instrument', 'direction', 'lot_size', 'profit', 'is_open']
