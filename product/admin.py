from django.contrib import admin
from product.models import Image, Product, Category, Brand, Color, Size, Variant

# Register your models here.
admin.site.register([Category, Brand, Color, Size, Image])


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'is_active')
    list_filter = ('brand', 'category')


class VariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'color', 'size', 'quantity')


admin.site.register(Product, ProductAdmin)
admin.site.register(Variant, VariantAdmin)
