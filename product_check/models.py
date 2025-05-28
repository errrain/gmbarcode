# product_check/models.py

from django.db import models
from django.contrib.auth import get_user_model

class BarcodeCheckLog(models.Model):
    CHECK_TYPE_CHOICES = (
        ('mix', '혼입 점검'),
        ('box', '포장 점검'),
    )
    check_type = models.CharField("점검 구분", max_length=10, choices=CHECK_TYPE_CHOICES)
    product = models.ForeignKey('product_info.Product', on_delete=models.CASCADE, verbose_name="제품")
    result = models.CharField("결과", max_length=10, default='오류')
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name="작업자")
    checked_at = models.DateTimeField("점검 시간", auto_now_add=True)

    def __str__(self):
        return f"[{self.get_check_type_display()}][{self.product.name}] {self.result} ({self.checked_at:%Y-%m-%d %H:%M})"
