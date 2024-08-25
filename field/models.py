# Create your models here.
from app.models import BaseModel
from cloudinary.models import CloudinaryField
from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User
from datetime import datetime


class Field(BaseModel):
    class FieldStatus(models.TextChoices):
        AVAILABLE = "Available", _("TRỐNG")
        BOOKED = "Booked", _("ĐÃ ĐẶT")
        MAINTENANCE = "Maintenance", _("ĐANG BẢO TRÌ")

    class FieldType(models.TextChoices):
        TYPE_5 = "5", _("Sân 5")
        TYPE_7 = "7", _("Sân 7")
        TYPE_11 = "11", _("Sân 11")

    name = models.CharField(max_length=50, unique=True)
    img = CloudinaryField(null=True)
    price = models.PositiveBigIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=FieldStatus.choices,
        default=FieldStatus.AVAILABLE,
    )
    field_type = models.CharField(
        max_length=20,
        choices=FieldType.choices,
        default=FieldType.TYPE_5,
    )
    __previous_status = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__previous_status = self.status

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.status != self.__previous_status:
            latest_history = (
                FieldStatusHistory.objects.filter(field=self.id).order_by("-id").first()
            )
            FieldStatusHistory.objects.create(
                field=self,
                status=self.__previous_status,
                start_date=latest_history.end_date if latest_history else None,
                end_date=datetime.now(),
            )

        super().save(force_insert, force_update, *args, **kwargs)
        self.__previous_status = self.status

    class Meta:
        verbose_name = _("Sân bóng")
        verbose_name_plural = _("Sân bóng")

    def __str__(self):
        return self.name

    def is_booked(self):
        return self.status == self.FieldStatus.BOOKED

    @property
    def img_url(self):
        if self.img:
            self.img.url_options.update({"secure": True})
            return self.img.url
        return self.img

    @property
    def avg_rating(self):
        rating = self.review_set.aggregate(models.Avg("rating")).get("rating__avg")
        return rating if rating is not None else 0.0


class FieldStatusHistory(BaseModel):
    field = models.ForeignKey(to=Field, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=Field.FieldStatus.choices,
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField()

    class Meta:
        verbose_name = _("Lịch sử trạng thái sân bóng")
        verbose_name_plural = _("Lịch sử trạng thái sân bóng")

    def __str__(self):
        return f"{self.field} - {self.status} from {self.start_date} to {self.end_date}"


class Booking(BaseModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    field = models.ForeignKey(to=Field, on_delete=models.CASCADE)
    from_time = models.TimeField()
    to_time = models.TimeField()
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False
    )
    booking_date = models.DateField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)
    booker_name = models.CharField(max_length=50, blank=False, null=False)
    phone_number = models.CharField(max_length=11, blank=False, null=False)
    paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Đặt sân bóng")
        verbose_name_plural = _("Đặt sân bóng")

    def __str__(self):
        return f"Booking by {self.booker_name} for {self.field} from {self.from_time} to {self.to_time}"

    def pay(self):
        self.paid = True
        self.save()
