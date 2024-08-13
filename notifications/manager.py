from notifications.models import (
    Notification,
    NotificationContent,
    NotificationSender,
)
from user.models import User


class NotificationManager:
    @staticmethod
    def get_users_by_target(filters=None):
        if filters is None:
            filters = {}
        return User.objects.filter(**filters).distinct()

    @staticmethod
    def create_notification(
        entity=None, entity_type=None, sender=None, image=None, filters=None
    ):
        if filters is None:
            filters = {}
        if not entity or not entity_type:
            raise ValueError("entity values must not be empty")
        if not sender:
            sender = User.objects.filter(is_staff=True).first()
        if not image:
            image = ""  # TODO: Set app logo for this
        content = NotificationContent.objects.create(
            entity_id=str(entity.pk),
            entity_type=entity_type,
            image=image,
        )
        NotificationSender.objects.create(user=sender, notification_content=content)
        users = NotificationManager.get_users_by_target(filters=filters)
        for user in users:
            Notification.objects.create(user=user, notification_content=content)
