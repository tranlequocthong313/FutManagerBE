from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from field.models import Field
from app.models import BaseModel


# Tạo các model tại đây


class Review(BaseModel):
    user = models.ForeignKey(
        verbose_name=" Người nhận đánh giá",
        to=get_user_model(),
        on_delete=models.CASCADE,
    )
    football_field = models.ForeignKey(
        verbose_name="Sân bóng", to=Field, on_delete=models.CASCADE
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    content = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Đánh giá"
        verbose_name_plural = "Đánh giá"
        ordering = ["-created_date"]  # Sắp xếp theo ngày tạo giảm dần
        unique_together = ["user", "football_field"]

    def __str__(self):
        return f"{self.user.__str__()} - {self.football_field} - {self.rating}"
