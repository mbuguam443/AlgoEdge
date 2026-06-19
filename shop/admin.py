from django.contrib import admin
from .models import ProductCategory, Product, ProductImage, Review

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'product_type', 'price', 'is_published', 'is_featured', 'download_count', 'rating']
    list_filter = ['is_published', 'is_featured', 'product_type', 'category']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ['title']}
    inlines = [ProductImageInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
