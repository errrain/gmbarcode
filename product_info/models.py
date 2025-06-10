from django.db import models
from django.conf import settings
from product_program.models import ProductProgram

class Product(models.Model):
    program = models.ForeignKey(ProductProgram, on_delete=models.CASCADE, verbose_name="프로그램명")
    name = models.CharField(max_length=200, verbose_name="제품명")
    image = models.ImageField(upload_to='product_images/', null=True, blank=True, verbose_name="제품 이미지")
    box_quantity = models.PositiveIntegerField(verbose_name="박스 포장 수량")
    pallet_box_quantity = models.PositiveIntegerField(null=True, blank=True, verbose_name="파레트 적재 박스 수량")  # ✅ 추가
    product_barcode = models.CharField(max_length=100, verbose_name="제품 바코드")
    box_barcode = models.CharField(max_length=100, verbose_name="포장 박스 바코드")

    is_active = models.BooleanField(default=True, verbose_name="사용 여부")
    is_deleted = models.BooleanField(default=False, verbose_name="삭제 여부")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='product_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='product_updated', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "제품"
        verbose_name_plural = "제품 목록"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.program.name} - {self.name}"
