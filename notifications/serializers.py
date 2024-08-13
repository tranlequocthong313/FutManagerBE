from rest_framework import serializers

from notifications.types import (
    ENTITY_TYPE_MODEL_MAPPINGS,
    ENTITY_TYPE_MESSAGE_MAPPINGS,
)

from .models import Notification, NotificationContent


class NotificationContentSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        r = super().to_representation(instance)
        if not r["image"]:
            r["image"] = ""  # TODO: Set app logo for this
        return r

    class Meta:
        model = NotificationContent
        fields = ["id", "entity_type", "entity_id", "image"]
        read_only_fields = ["id", "entity_type", "entity_id", "image"]


class NotificationSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField(read_only=True)
    content = NotificationContentSerializer(read_only=True)

    def get_message(self, instance):
        entity = ENTITY_TYPE_MODEL_MAPPINGS[
            instance.notification_content.entity_type
        ].objects.get(pk=instance.notification_content.entity_id)
        return ENTITY_TYPE_MESSAGE_MAPPINGS[instance.notification_content.entity_type](
            entity, instance.notification_content
        )

    class Meta:
        model = Notification
        fields = [
            "id",
            "read",
            "message",
            "content",
            "created_date",
            "updated_date",
        ]
        read_only_fields = [
            "id",
            "read",
            "message",
            "content",
            "created_date",
            "updated_date",
        ]
