from django.db import models
from django.contrib.auth.models import User

class UserBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    content_type = models.CharField(max_length=50)
    object_id = models.IntegerField()
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'content_type', 'object_id']

class UserDownload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='downloads')
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    downloaded_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        ordering = ['-downloaded_at']
