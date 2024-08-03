from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User
from app.models import BaseModel
from cloudinary.models import CloudinaryField


# Create your models here.


class NotificationContent(BaseModel):
    class EntityType(models.TextChoices):
        BOOKING = 'booking', _('Booking')
        REVIEW = 'review', _('Review')
        REVIEW_EDIT = 'review_edit', _('Review Edit')

    entity_id = models.PositiveIntegerField()
    name = models.CharField(max_length=200, blank=False, null=False)
    image = CloudinaryField(null=True)
    entity_type = models.CharField(
        max_length=20,
        choices=EntityType.choices,
        null=False
    )

    def __str__(self):
        return f"{self.name} - {self.entity_type}"


class Notification(BaseModel):
    class RecipientType(models.TextChoices):
        CUSTOMER = 'customer', _('Customer')
        MANAGER = 'manager', _('Manager')

    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_content = models.ForeignKey(NotificationContent, on_delete=models.CASCADE)
    recipient_type = models.CharField(
        max_length=20,
        choices=RecipientType.choices,
        null=False
    )

    def __str__(self):
        return f"Notification for {self.user} - {self.recipient_type}"


class NotificationRecipient(BaseModel):
    notification_content = models.ForeignKey(NotificationContent, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # class Meta:
    #     unique_together = ('notification', 'user')

    def __str__(self):
        return f"Notification {self.notification_content.id} to {self.user.username}"
