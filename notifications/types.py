# notification/types.py

from django.utils.translation import gettext_lazy as _
from django.db import models
from field.models import Booking
from review.models import Review


class EntityType(models.TextChoices):
    BOOKING = "booking", _("Đã đặt sân")
    REVIEW = "review", _("Đã đánh giá sân")
    REVIEW_EDIT = "review_edit", _("Chỉnh sửa đánh giá sân")


class SendType(models.TextChoices):
    USER = "USER", _("Người dùng")
    ADMIN = "ADMIN", _("Ban quản trị")
    CUSTOMER = "CUSTOMER", _("Khách hàng")
    CUSTOMERS = "CUSTOMERS", _("Nhiều khách hàng")
    ALL = "ALL", _("Tất cả")


ENTITY_TYPE_MODEL_MAPPINGS = {
    EntityType.BOOKING: Booking,
    EntityType.REVIEW: Review,
    EntityType.REVIEW_EDIT: Review,
}

ENTITY_TARGET_MAPPINGS = {
    EntityType.BOOKING: SendType.ADMIN,
    EntityType.REVIEW: SendType.ADMIN,
    EntityType.REVIEW_EDIT: SendType.ADMIN,
}

ENTITY_TYPE_MESSAGE_MAPPINGS = {
    EntityType.BOOKING: lambda entity,
    content: f"{entity.user.__str__()} {content.get_entity_type_display().lower()} {entity.field.__str__()}",
    EntityType.REVIEW: lambda entity,
    content: f"{entity.user.__str__()} {content.get_entity_type_display().lower()} {entity.field.__str__()}",
    EntityType.REVIEW_EDIT: lambda entity,
    content: f"{entity.user.__str__()} {content.get_entity_type_display().lower()} {entity.field.__str__()}",
}
