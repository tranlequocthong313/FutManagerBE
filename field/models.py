from django.db import models

# Create your models here.

from django.db import models
from cloudinary.models import CloudinaryField
from app.models import BaseModel
from user.models import User
from django.utils.translation import gettext_lazy as _


class Field(BaseModel):
    class FieldStatus(models.TextChoices):
        AVAILABLE = 'available', _('Available')
        BOOKED = 'booked', _('Booked')
        UNDER_MAINTENANCE = 'under_maintenance', _('Under Maintenance')

    class FieldType(models.TextChoices):
        TYPE_5 = '5', _('5-a-side')
        TYPE_7 = '7', _('7-a-side')
        TYPE_11 = '11', _('11-a-side')

    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
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

    def __str__(self):
        return self.name


class FieldStatusHistory(BaseModel):
    football_field = models.ForeignKey(Field, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=Field.FieldStatus.choices,
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.football_field} - {self.status} from {self.start_date} to {self.end_date}"


class Booking(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    football_field = models.ForeignKey(Field, on_delete=models.CASCADE)
    from_time = models.DateTimeField(blank=False, null=False)
    to_time = models.DateTimeField(blank=False, null=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    booking_date = models.DateField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)
    booker_name = models.CharField(max_length=150, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=False, null=False)

    def __str__(self):
        return f"Booking by {self.booker_name} for {self.football_field} from {self.from_time} to {self.to_time}"
