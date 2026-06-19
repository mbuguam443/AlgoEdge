import time
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.conf import settings

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR', '')
        key = f'ratelimit_{ip}'
        now = time.time()
        history = cache.get(key, [])
        history = [t for t in history if t > now - 60]
        if len(history) > 60:
            return HttpResponseForbidden('Rate limit exceeded')
        history.append(now)
        cache.set(key, history, 60)
        return self.get_response(request)
