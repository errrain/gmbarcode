from django.db import models
from django.conf import settings
from product_info.models import Product

class ShippingSession(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    box_count = models.PositiveIntegerField(default=0)  # 총 박스 수량
    pallet_count = models.PositiveIntegerField(default=0)  # 총 팔레트 수량
    created_at = models.DateTimeField(auto_now_add=True)  # 저장된 시간

    def __str__(self):
        return f"{self.created_at.strftime('%Y%m%d-%H%M')} | {self.product.name} | {self.user}"


class ShippingLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    box_count = models.PositiveIntegerField(default=0)
    pallet_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at.strftime('%Y-%m-%d %H:%M')} | {self.product.name} | {self.user.full_name if self.user else 'Unknown'}"