from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from .sitemaps import sitemaps

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('userauth.urls')),
    path('academy/', include('learn.urls')),
    path('marketplace/', include('shop.urls')),
    path('services/', include('cservice.urls')),
    path('blog/', include('articles.urls')),
    path('dashboard/', include('dash.urls')),
    path('copytrading/', include('copytrade.urls')),
    path('propfirm/', include('pfarm.urls')),
    path('automation/', include('automate.urls')),
    path('broker/', include('brokerx.urls')),
    path('affiliates/', include('refer.urls')),
    path('notifications/', include('alerts.urls')),
    path('payments/', include('paygate.urls')),
    path('analytics/', include('metrics.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
