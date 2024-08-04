# notification/types.py

from django.utils.translation import gettext_lazy as _
from django.db import models


class EntityType(models.TextChoices):
    BOOKING = 'booking', _('Đã đặt sân')
    REVIEW = 'review', _('Đã đánh giá')
    REVIEW_EDIT = 'review_edit', _('Chỉnh sửa đánh giá')


class SendType(models.TextChoices):
    UNICAST = 'unicast', _('Unicast')
    MULTICAST = 'multicast', _('Multicast')
    BROADCAST = 'broadcast', _('Broadcast')
