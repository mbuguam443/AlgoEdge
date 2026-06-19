from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Notification

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'alerts/notifications.html'
    context_object_name = 'notifications'
    paginate_by = 20
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

def mark_read(request, pk):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, pk=pk).update(is_read=True)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)

def mark_all_read(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)
