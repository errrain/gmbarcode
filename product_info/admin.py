from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'program', 'box_quantity', 'is_active', 'is_deleted')
    list_filter = ('program', 'is_active', 'is_deleted')
    search_fields = ('name', 'product_barcode', 'box_barcode')
