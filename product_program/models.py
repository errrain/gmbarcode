from django.db import models
from django.conf import settings


class ProductProgram(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="프로그램명")
    description = models.TextField(blank=True, verbose_name="설명")

    is_active = models.BooleanField(default=True, verbose_name="사용 여부")
    is_deleted = models.BooleanField(default=False, verbose_name="삭제 여부")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_product_programs',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="작성자"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='updated_product_programs',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="수정자"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "제품 프로그램"
        verbose_name_plural = "제품 프로그램 목록"
