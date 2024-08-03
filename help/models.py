from django.db import models
from app.models import BaseModel


# Create your models here.
class HelpCategory(BaseModel):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name


class Help(BaseModel):
    category = models.ForeignKey(HelpCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=False)
    content = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.title
