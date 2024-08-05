from app.models import BaseModel
from django.db import models

# Tạo các model tại đây


class HelpCategory(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Danh mục trợ giúp"
        verbose_name_plural = "Danh mục trợ giúp"
        ordering = ["name"]  # Sắp xếp theo tên mặc định

    def __str__(self):
        return self.name


class Help(BaseModel):
    category = models.ForeignKey(
        to=HelpCategory, on_delete=models.CASCADE, related_name="helps"
    )
    title = models.CharField(max_length=50, blank=False, null=False)
    content = models.TextField(blank=False, null=False)

    class Meta:
        verbose_name = "Trợ giúp"
        verbose_name_plural = "Trợ giúp"
        ordering = ["title"]  # Sắp xếp theo tiêu đề mặc định

    def __str__(self):
        return self.title
