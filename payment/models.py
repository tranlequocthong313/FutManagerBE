from django.db import models
from field.models import Booking
from django.utils.translation import gettext_lazy as _
from app.models import BaseModel


# Create your models here.
class Payment(BaseModel):
    class PaymentStatus(models.TextChoices):
        SUCCESS = 'success', _('Success')
        PENDING = 'pending', _('Pending')
        FAILED = 'failed', _('Failed')

    class PaymentChannel(models.TextChoices):
        MOMO = 'momo', _('Momo')
        VN_PAY = 'vn_pay', _('VNPay')

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )
    channel = models.CharField(
        max_length=20,
        choices=PaymentChannel.choices,
        default=PaymentChannel.MOMO,
    )
    transaction_id = models.CharField(max_length=100, blank=False, null=False)
    reference_code = models.CharField(max_length=100, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.transaction_id} for Booking {self.booking.id}"
