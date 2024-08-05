from app.models import BaseModel
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from field.models import Field

# Tạo các model tại đây


class Review(BaseModel):
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
    )
    field = models.ForeignKey(to=Field, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Đánh giá"
        verbose_name_plural = "Đánh giá"
        ordering = ["-created_date"]  # Sắp xếp theo ngày tạo giảm dần
        unique_together = ["user", "field"]

    def __str__(self):
        return f"{self.user.__str__()} - {self.field} - {self.rating}"
