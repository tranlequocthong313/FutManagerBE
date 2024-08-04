from django.db import models
from app.models import BaseModel


# Tạo các model tại đây

class Introduction(BaseModel):
    content = models.TextField()
    version = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Giới thiệu"
        verbose_name_plural = "Giới thiệu"
        ordering = ['-created_date']  # Sắp xếp theo ngày tạo giảm dần

    def __str__(self):
        return f"Version {self.version}"


class CustomerSupport(BaseModel):
    service_name = models.CharField(max_length=50)
    content = models.TextField()

    class Meta:
        verbose_name = "Hỗ trợ khách hàng"
        verbose_name_plural = "Hỗ trợ khách hàng"
        ordering = ['service_name']  # Sắp xếp theo tên dịch vụ

    def __str__(self):
        return self.service_name
