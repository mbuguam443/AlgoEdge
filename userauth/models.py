from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    wallet_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    lifetime_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    mt4_account = models.CharField(max_length=50, blank=True)
    mt5_account = models.CharField(max_length=50, blank=True)
    broker_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"

class EAWallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ea_wallets')
    product = models.CharField(max_length=200)
    license_key = models.CharField(max_length=100, unique=True)
    mt4_account = models.CharField(max_length=50, blank=True)
    mt5_account = models.CharField(max_length=50, blank=True)
    hardware_id = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    activated_at = models.DateTimeField(auto_now_add=True)
    last_validated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'EA Wallet'
        verbose_name_plural = 'EA Wallets'

    def __str__(self):
        return f"{self.user.username} - {self.product}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
