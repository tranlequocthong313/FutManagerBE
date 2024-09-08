# notification/types.py

from django.utils.translation import gettext_lazy as _
from django.db import models
from field.models import Booking
from review.models import Review


class EntityType(models.TextChoices):
    BOOKING = "booking", _("Đã đặt sân")
    CONFIRM_BOOKING = "confirm_booking", _("Chúc mừng bạn đã đăt sân thành công")
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
    EntityType.CONFIRM_BOOKING: Booking,
    EntityType.REVIEW: Review,
    EntityType.REVIEW_EDIT: Review,
}

ENTITY_TARGET_MAPPINGS = {
    EntityType.BOOKING: SendType.ADMIN,
    EntityType.CONFIRM_BOOKING: SendType.CUSTOMER,
    EntityType.REVIEW: SendType.ADMIN,
    EntityType.REVIEW_EDIT: SendType.ADMIN,
}

ENTITY_TYPE_MESSAGE_MAPPINGS = {
    EntityType.BOOKING: lambda entity,
    content: f"{entity.user.__str__()} {content.get_entity_type_display().lower()} {entity.field.__str__()}",
    EntityType.CONFIRM_BOOKING: lambda entity,
    content: f"{content.get_entity_type_display()} ({entity.field.__str__()} | {entity.booking_date.strftime('%d/%m/%Y')} | {entity.from_time.strftime('%Hh')}-{entity.to_time.strftime('%Hh')})",
    EntityType.REVIEW: lambda entity,
    content: f"{entity.user.__str__()} {content.get_entity_type_display().lower()} {entity.field.__str__()}",
    EntityType.REVIEW_EDIT: lambda entity,
    content: f"{entity.user.__str__()} {content.get_entity_type_display().lower()} {entity.field.__str__()}",
}
