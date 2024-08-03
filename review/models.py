from django.db import models
from django.contrib.auth import get_user_model
from field.models import Field
from app.models import BaseModel


# Create your models here.
class Review(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    football_field = models.ForeignKey(Field, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    content = models.TextField()

    def __str__(self):
        return f"{self.user} - {self.football_field} - {self.rating}"
