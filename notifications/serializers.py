from rest_framework import serializers

from notifications.types import (
    ENTITY_TYPE_MODEL_MAPPINGS,
    ENTITY_TYPE_MESSAGE_MAPPINGS,
)
from app import settings
from .models import Notification, NotificationContent, FCMToken


class NotificationContentSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        r = super().to_representation(instance)
        r["image"] = instance.img_url if instance.image else settings.LOGO
        return r

    class Meta:
        model = NotificationContent
        fields = ["id", "entity_type", "entity_id", "image"]
        read_only_fields = ["id", "entity_type", "entity_id", "image"]


class NotificationSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField(read_only=True)
    content = NotificationContentSerializer(
        read_only=True, source="notification_content"
    )

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


class ReadNotificationSerializer(serializers.Serializer):
    notification_content_id = serializers.IntegerField()


class FCMTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMToken
        fields = ["id", "token"]

    def create(self, validated_data):
        obj, created = FCMToken.objects.update_or_create(
            token=validated_data["token"],
            defaults={
                "token": validated_data["token"],
                "user": validated_data["user"],
            },
            create_defaults={
                "token": validated_data["token"],
                "user": validated_data["user"],
            },
        )
        return obj, created
