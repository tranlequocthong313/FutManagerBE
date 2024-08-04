from django.db import models
from field.models import Booking
from django.utils.translation import gettext_lazy as _
from app.models import BaseModel


# Tạo các model tại đây

class Payment(BaseModel):
    class PaymentStatus(models.TextChoices):
        SUCCESS = 'success', _('Thành công')
        PENDING = 'pending', _('Đang thanh toán')
        FAILED = 'failed', _('Không thành công')

    class PaymentChannel(models.TextChoices):
        MOMO = 'momo', _('Momo')
        VN_PAY = 'vn_pay', _('VNPay')

    booking = models.ForeignKey(verbose_name="Đặt sân bóng", to=Booking, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
    )
    channel = models.CharField(
        max_length=20,
        choices=PaymentChannel.choices,
    )
    transaction_id = models.CharField(max_length=50, blank=False, null=False)
    reference_code = models.CharField(max_length=50, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Thanh toán"
        verbose_name_plural = "Thanh toán"
        ordering = ['-created_at']  # Sắp xếp theo ngày tạo giảm dần

    def __str__(self):
        return f"Payment {self.transaction_id} for Booking {self.booking.id}"
