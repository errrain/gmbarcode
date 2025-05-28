# product_check/admin.py

from django.contrib import admin
from .models import BarcodeCheckLog

@admin.register(BarcodeCheckLog)
class BarcodeCheckLogAdmin(admin.ModelAdmin):
    list_display = ('checked_at', 'check_type', 'product', 'user', 'result')
    list_filter = ('check_type', 'result', 'user')
    search_fields = ('product__name', 'user__username')
    ordering = ('-checked_at',)