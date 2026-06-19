from django.db import models
from django.contrib.auth.models import User

class BrokerVerification(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='broker_verifications')
    broker_name = models.CharField(max_length=200)
    account_number = models.CharField(max_length=50)
    account_type = models.CharField(max_length=20, choices=[('mt4', 'MT4'), ('mt5', 'MT5'), ('ctrader', 'cTrader')], default='mt5')
    account_size = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    screenshot = models.ImageField(upload_to='broker_verifications/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.broker_name} ({self.account_number})"

class AffiliateReferral(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='affiliate_referrals')
    referred_email = models.EmailField()
    referred_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='referred_by_affiliate')
    broker_verified = models.BooleanField(default=False)
    commission_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} referred {self.referred_email}"

class Payout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payouts')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50)
    account_details = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('processed', 'Processed'), ('cancelled', 'Cancelled')], default='pending')
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
