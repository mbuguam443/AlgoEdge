from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class MasterTrader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='master_trader', null=True, blank=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='traders/', blank=True, null=True)
    broker = models.CharField(max_length=100, blank=True)
    trading_style = models.CharField(max_length=100, blank=True)
    instruments = models.CharField(max_length=300, blank=True)
    roi = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    win_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    max_drawdown = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    profit_factor = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    sharpe_ratio = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    total_trades = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    monthly_roi = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    min_investment = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    fee_percentage = models.DecimalField(max_digits=4, decimal_places=2, default=20.00)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    risk_level = models.CharField(max_length=20, default='moderate')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-roi']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class CopySubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='copy_subscriptions')
    trader = models.ForeignKey(MasterTrader, on_delete=models.CASCADE, related_name='subscriptions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    total_pnl = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ['user', 'trader']

    def __str__(self):
        return f"{self.user.username} copies {self.trader.name}"

class PerformanceHistory(models.Model):
    trader = models.ForeignKey(MasterTrader, on_delete=models.CASCADE, related_name='performance_history')
    date = models.DateField()
    equity = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    daily_pnl = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    drawdown = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    trades_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['date']
        unique_together = ['trader', 'date']

class Signal(models.Model):
    trader = models.ForeignKey(MasterTrader, on_delete=models.CASCADE, related_name='signals')
    instrument = models.CharField(max_length=50)
    direction = models.CharField(max_length=10, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    entry_price = models.DecimalField(max_digits=12, decimal_places=5)
    stop_loss = models.DecimalField(max_digits=12, decimal_places=5)
    take_profit = models.DecimalField(max_digits=12, decimal_places=5)
    lot_size = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('closed', 'Closed'), ('pending', 'Pending')], default='pending')
    pnl = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
