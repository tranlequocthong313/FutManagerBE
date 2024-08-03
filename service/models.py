from django.db import models
from app.models import BaseModel


# Create your models here.
class Introduction(BaseModel):
    content = models.TextField(blank=False, null=False)
    version = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return f"Version {self.version}"


class CustomerService(BaseModel):
    service_name = models.CharField(max_length=100, blank=False, null=False)
    content = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.service_name
