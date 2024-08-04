from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'customer', _('Khách hàng')
        ADMIN = 'admin', _('Quản Trị Viên')

    full_name = models.CharField(max_length=50, default="None")
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    # email có trong Abstract rồi nha
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )

    class Meta:
        verbose_name = "Người dùng"
        verbose_name_plural = "Người dùng"

    def __str__(self):
        return f"{self.full_name}"
