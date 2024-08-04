from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User
from app.models import BaseModel
from cloudinary.models import CloudinaryField
from .types import EntityType, SendType  # Import các Enum types


# Tạo các model tại đây


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
        max_length=20, choices=SendType.choices, default=SendType.UNICAST
    )

    class Meta:
        verbose_name = "Thông báo"
        verbose_name_plural = "Thông báo"
        # unique_together = ('user', 'notification_content')  # Đảm bảo duy nhất giữa người dùng và nội dung thông báo

    def __str__(self):
        return f"Notification for {self.user} - {self.send_type}"


class NotificationRecipient(BaseModel):
    notification_content = models.ForeignKey(
        to=NotificationContent, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        verbose_name=" Người nhận thông báo", to=User, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Người nhận thông báo"
        verbose_name_plural = "Người nhận thông báo"
        # unique_together = ('notification_content', 'user')  # Đảm bảo duy nhất giữa nội dung thông báo và người nhận

    def __str__(self):
        return f"Notification {self.notification_content.id} to {self.user.fullname}"
