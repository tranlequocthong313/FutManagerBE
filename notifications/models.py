from django.core.validators import MinLengthValidator
from app.models import BaseModel
from cloudinary.models import CloudinaryField
from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User

from .types import EntityType, SendType  # Import các Enum types


# Tạo các model tại đây
class FCMToken(BaseModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    token = models.CharField(
        max_length=163, unique=True, validators=[MinLengthValidator(163)]
    )

    def __str__(self) -> str:
        return f"{self.user.__str__()} - {self.device_type}"


class NotificationContent(BaseModel):
    entity_id = models.CharField(max_length=100, blank=False, null=False)
    image = CloudinaryField(null=True)
    entity_type = models.CharField(
        max_length=255, choices=EntityType.choices, null=False
    )

    class Meta:
        verbose_name = "Nội dung thông báo"
        verbose_name_plural = "Nội dung thông báo"
        # unique_together = ('entity_id', 'entity_type')  # Đảm bảo tính duy nhất của entity_id và entity_type

    def __str__(self):
        return f"{self.entity_id} - {self.entity_type}"


class Notification(BaseModel):
    read = models.BooleanField(default=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    notification_content = models.ForeignKey(
        verbose_name="Nội dung thông báo",
        to=NotificationContent,
        on_delete=models.CASCADE,
    )
    send_type = models.CharField(
        max_length=20, choices=SendType.choices, default=SendType.USER
    )

    class Meta:
        verbose_name = "Thông báo"
        verbose_name_plural = "Thông báo"
        # unique_together = ('user', 'notification_content')  # Đảm bảo duy nhất giữa người dùng và nội dung thông báo

    def __str__(self):
        return f"Notification for {self.user} - {self.send_type}"


class NotificationSender(BaseModel):
    notification_content = models.ForeignKey(
        to=NotificationContent, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        verbose_name=" Người gửi thông báo", to=User, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Người gửi thông báo"
        verbose_name_plural = "Người gửi thông báo"

    def __str__(self):
        return f"Notification {self.notification_content.id} to {self.user.fullname}"
