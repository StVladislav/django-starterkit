from django.contrib import admin
from django.utils.html import format_html

from src.examples.models import Product, ProductCategory, ProductImage


"""
Register model without any settings only for testing in the django admin.
"""


class ProductCategoryAdmin(admin.ModelAdmin):
    pass


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'name', 'slug', 'category__name', 'images_count', 'image_preview')
    inlines = [ProductImageInline, ]

    def images_count(self, obj):
        return obj.images.count()
    
    images_count.short_description = 'Number of images'
    
    def image_preview(self, obj):
        image_obj = obj.images.filter(is_main=True).first()
        if not image_obj:
            image_obj = obj.images.first()
        if not image_obj:
            return None
        return format_html(f'<img src="{image_obj.image.url}" width="50" style="margin-right: 2px;" />')

    image_preview.short_description = "Preview"


class ProductImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
