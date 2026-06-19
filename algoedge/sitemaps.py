from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from learn.models import Course
from shop.models import Product
from cservice.models import Service
from articles.models import Post
from pfarm.models import PropFirm
from copytrade.models import MasterTrader


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'home:index', 'home:about', 'home:contact', 'home:faq', 'home:pricing',
            'cservice:services', 'learn:courses', 'shop:products',
            'copytrade:traders', 'pfarm:firms', 'articles:blog',
        ]

    def location(self, item):
        return reverse(item)


class CourseSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Course.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Product.objects.filter(is_published=True)


class ServiceSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Service.objects.all()


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Post.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at


class PropFirmSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return PropFirm.objects.filter(is_active=True)


class MasterTraderSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7

    def items(self):
        return MasterTrader.objects.filter(is_active=True)


sitemaps = {
    'static': StaticViewSitemap(),
    'courses': CourseSitemap(),
    'products': ProductSitemap(),
    'services': ServiceSitemap(),
    'posts': PostSitemap(),
    'propfirms': PropFirmSitemap(),
    'traders': MasterTraderSitemap(),
}
