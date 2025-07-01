from django.contrib import admin

from src._test.models import Product, ProductCategory


"""
Register model without any settings only for testing in the django admin.
"""


class ProductCategoryAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'name', 'slug', 'category__name', 'image')


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
