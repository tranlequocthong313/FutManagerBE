import json

from .types import SendType, ENTITY_TARGET_MAPPINGS, ENTITY_TYPE_MESSAGE_MAPPINGS
from notifications.models import (
    FCMToken,
    Notification,
    NotificationContent,
    NotificationSender,
)
from user.models import User
from firebase import message
from .serializers import NotificationContentSerializer
from app import settings
from django.db.models import Q


class NotificationManager:
    @staticmethod
    def get_users_by_target(target=None, filters=None):
        if filters is None:
            filters = {}
        return (
            User.objects.filter(
                Q(is_staff=True) | Q(role="admin"), **filters
            ).distinct()
            if target == SendType.ADMIN
            else User.objects.filter(**filters).distinct()
        )

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
            image = settings.LOGO
        target = ENTITY_TARGET_MAPPINGS[str(entity_type)]
        content = NotificationContent.objects.create(
            entity_id=str(entity.pk),
            entity_type=entity_type,
            image=image,
        )
        NotificationSender.objects.create(user=sender, notification_content=content)
        users = NotificationManager.get_users_by_target(target=target, filters=filters)
        for user in users:
            Notification.objects.create(
                user=user, notification_content=content, send_type=target
            )
        tokens = None
        if len(users) > 0 and target == SendType.CUSTOMER:
            tokens = (
                FCMToken.objects.filter(user=users[0])
                .values_list("token", flat=True)
                .all()
            )
        message.send_notification(
            tokens=tokens,
            target=target,
            title=ENTITY_TYPE_MESSAGE_MAPPINGS[entity_type](
                entity=entity, content=content
            ),
            image=image,
            data={"content": json.dumps(NotificationContentSerializer(content).data)},
        )
