from django.views.generic import ListView, DetailView
from .models import Product, ProductCategory

class ProductListView(ListView):
    model = Product
    template_name = 'shop/products.html'
    context_object_name = 'products'
    paginate_by = 12
    def get_queryset(self):
        qs = Product.objects.filter(is_published=True)
        cat = self.request.GET.get('category')
        kind = self.request.GET.get('type')
        if cat: qs = qs.filter(category__slug=cat)
        if kind: qs = qs.filter(product_type=kind)
        return qs

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

class CategoryListView(ListView):
    model = ProductCategory
    template_name = 'shop/categories.html'
    context_object_name = 'categories'
