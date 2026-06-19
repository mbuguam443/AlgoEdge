from django.db import models
from django.contrib.auth.models import User

class PropFirm(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='propfirms/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PropFirmChallenge(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('verification', 'Verification Stage'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prop_challenges')
    firm = models.ForeignKey(PropFirm, on_delete=models.CASCADE, related_name='challenges')
    account_number = models.CharField(max_length=50)
    account_size = models.DecimalField(max_digits=12, decimal_places=2)
    challenge_type = models.CharField(max_length=50, default='Phase 1')
    profit_target = models.DecimalField(max_digits=6, decimal_places=2)
    daily_drawdown_limit = models.DecimalField(max_digits=6, decimal_places=2)
    max_drawdown_limit = models.DecimalField(max_digits=6, decimal_places=2)
    current_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    current_daily_drawdown = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    current_max_drawdown = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    peak_equity = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    days_remaining = models.IntegerField(default=30)
    total_days = models.IntegerField(default=30)
    trading_platform = models.CharField(max_length=20, default='MT5')
    ea_running = models.BooleanField(default=False)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.firm.name} ({self.account_size})"

class DailyEquity(models.Model):
    challenge = models.ForeignKey(PropFirmChallenge, on_delete=models.CASCADE, related_name='daily_equity')
    date = models.DateField()
    equity = models.DecimalField(max_digits=12, decimal_places=2)
    daily_pnl = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    drawdown = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Daily Equities'
        unique_together = ['challenge', 'date']
        ordering = ['date']

class TradeRecord(models.Model):
    challenge = models.ForeignKey(PropFirmChallenge, on_delete=models.CASCADE, related_name='trades')
    instrument = models.CharField(max_length=50)
    direction = models.CharField(max_length=10, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    lot_size = models.DecimalField(max_digits=6, decimal_places=2)
    entry_price = models.DecimalField(max_digits=12, decimal_places=5)
    exit_price = models.DecimalField(max_digits=12, decimal_places=5, null=True, blank=True)
    stop_loss = models.DecimalField(max_digits=12, decimal_places=5, null=True, blank=True)
    take_profit = models.DecimalField(max_digits=12, decimal_places=5, null=True, blank=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_open = models.BooleanField(default=True)
    open_time = models.DateTimeField()
    close_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-open_time']
