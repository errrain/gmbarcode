from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('worker', '작업자'),
        ('admin', '관리자'),
    )

    STATUS_CHOICES = (
        ('approved', '승인'),
        ('pending', '미승인'),
    )

    full_name = models.CharField("이름", max_length=50)
    user_type = models.CharField("구분", max_length=10, choices=USER_TYPE_CHOICES, default='worker')
    status = models.CharField("상태", max_length=10, choices=STATUS_CHOICES, default='pending')
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField("삭제여부", default=False)
    updated_at = models.DateTimeField("수정일시", auto_now=True)
    created_at = models.DateTimeField("생성일시", auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.full_name})"
