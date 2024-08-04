from django.db import models
from app.models import BaseModel


# Tạo các model tại đây

class HelpCategory(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Danh mục trợ giúp"
        verbose_name_plural = "Danh mục trợ giúp"
        ordering = ['name']  # Sắp xếp theo tên mặc định

    def __str__(self):
        return self.name


class Help(BaseModel):
    category = models.ForeignKey(verbose_name="Danh mục trợ giúp", to=HelpCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=False, null=False)
    content = models.TextField(blank=False, null=False)

    class Meta:
        verbose_name = "Trợ giúp"
        verbose_name_plural = "Trợ giúp"
        ordering = ['title']  # Sắp xếp theo tiêu đề mặc định

    def __str__(self):
        return self.title
