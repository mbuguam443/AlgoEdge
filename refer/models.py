from django.db import models
from django.contrib.auth.models import User

class AffiliateAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='affiliate_account')
    code = models.CharField(max_length=20, unique=True)
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    pending_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_referrals = models.IntegerField(default=0)
    commission_rate = models.DecimalField(max_digits=4, decimal_places=2, default=10.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.code}"
