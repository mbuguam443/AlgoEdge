from django.conf import settings
from alerts.models import Notification

def site_settings(request):
    return {
        'site_name': settings.SITE_NAME,
        'site_url': settings.SITE_URL,
        'discord_link': settings.DISCORD_INVITE_LINK,
        'telegram_link': settings.TELEGRAM_INVITE_LINK,
        'broker_affiliate_link': settings.BROKER_AFFILIATE_LINK,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'og_image_default': settings.STATIC_URL + 'logos/og-image.png',
    }

def notification_count(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'unread_notifications': count}
    return {'unread_notifications': 0}
