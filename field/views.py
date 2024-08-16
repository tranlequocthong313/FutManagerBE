from datetime import datetime
from calendar import monthrange
from django.db.models import Avg, Sum
from django.db.models import Count
from django.db.models.base import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.utils import timezone
from notifications.manager import NotificationManager
from notifications.types import EntityType
from payment.services import PaymentService
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from field.models import Booking, Field, FieldStatusHistory
from field.serializers import (
    BookingListSerializer,
    BookingSerializer,
    FieldSerializer,
)


# Create your views here.
class FieldView(ListAPIView, ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FieldSerializer
    paymentService = PaymentService()

    # NOTE:
    # - type: Loại sân (ví dụ: sân 5, sân 7)
    # - status: Trạng thái sân (ví dụ: Có sẵn, Đã được đặt, Bảo trì)
    # - toprice: Giá tối đa (ví dụ: 300000)
    # - fromrating: Đánh giá (ví du: 1, 3, 5)
    def get_queryset(self):
        queryset = Field.objects.all()

        if type := self.request.query_params.get("type"):
            queryset = queryset.filter(field_type=type)
        if status := self.request.query_params.get("status"):
            queryset = queryset.filter(status=status)
        if from_price := self.request.query_params.get("fromprice"):
            queryset = queryset.filter(price__gte=from_price)
        if to_price := self.request.query_params.get("toprice"):
            queryset = queryset.filter(price__lte=to_price)
        if from_rating := self.request.query_params.get("fromrating"):
            queryset = queryset.annotate(rating=Avg("review__rating")).filter(
                rating__gte=from_rating
            )

        return queryset

    def overlapping_bookings(self, data):
        return Booking.objects.filter(
            field=data["field"],
            booking_date=data["booking_date"],
            from_time__lt=data["to_time"],
            to_time__gt=data["from_time"],
            paid=True,
        ).exists()

    def calculate_total_amount(self, from_time, to_time, price):
        duration = (
            datetime.combine(datetime.min, to_time)
            - datetime.combine(datetime.min, from_time)
        ).seconds / 3600
        return duration * price

    @action(
        url_path="book",
        methods=["post"],
        detail=True,
    )
    def book_field(self, request, pk=None):
        field = get_object_or_404(Field, pk=pk)
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["field"] = field
            from_time = serializer.validated_data["from_time"]
            to_time = serializer.validated_data["to_time"]
            payment_channel = serializer.validated_data["payment_channel"]

            if self.overlapping_bookings(serializer.validated_data):
                return Response(
                    {"status": 400, "message": "Time slot has been reserved"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            total_amount = self.calculate_total_amount(from_time, to_time, field.price)
            booking = serializer.save(
                user=request.user, field=field, total_amount=total_amount
            )
            return self.paymentService.pay(request, booking, payment_channel)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        url_path="bookings",
        methods=["get"],
        detail=True,
        permission_classes=[AllowAny],
    )
    def bookings(self, request, pk=None):
        field = get_object_or_404(Field, pk=pk)
        if date_str := request.query_params.get("date"):
            try:
                booking_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return Response(
                    {"status": 400, "message": "Invalid date format. Use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            booking_date = timezone.now().date()

        bookings = Booking.objects.filter(
            field=field, booking_date=booking_date, paid=True
        )
        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        url_path="revenue/stats",
        methods=["get"],
        detail=False,
        permission_classes=[IsAuthenticated],  # Đảm bảo người dùng đã xác thực
    )
    def revenue_stats(self, request):
        year = request.query_params.get("year")
        month = request.query_params.get("month")

        if not year or not month:
            return Response(
                {"status": 400, "message": "Invalid query params"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            year = int(year)
            month = int(month)
            if month < 1 or month > 12:
                raise ValueError("Invalid month value")
        except ValueError:
            return Response(
                {"status": 400, "message": "Invalid query params"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            bookings = Booking.objects.filter(
                booking_date__year=year, booking_date__month=month, paid=True
            )

            monthly_revenue = (
                bookings.aggregate(total_revenue=Sum("total_amount"))["total_revenue"]
                or 0
            )
            daily_revenue = (
                bookings.values("booking_date__day")
                .annotate(total_revenue=Sum("total_amount"))
                .order_by("booking_date__day")
            )

            daily_revenue_list = [
                {
                    "day": day["booking_date__day"],
                    "total_revenue": float(day["total_revenue"]),
                }
                for day in daily_revenue
            ]
            response_data = {
                "year": year,
                "monthly_revenue": [
                    {
                        "month": month,
                        "total_revenue": float(monthly_revenue),
                        "daily_revenue": daily_revenue_list,
                    }
                ],
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception:
            return Response(
                {"status": 500, "message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(
        methods=["get"],
        detail=True,
        url_path="statuses/stats",
        url_name="statuses_stats",
    )
    def statuses_stats(self, request, pk=None):
        month = request.query_params.get("month")
        year = request.query_params.get("year")

        if not month or not year:
            current_date = datetime.now()
            month = month or current_date.month
            year = year or current_date.year
        else:
            try:
                month = int(month)
                year = int(year)
            except ValueError:
                return Response(
                    {"status": 400, "message": "Invalid query params"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        days_in_month = monthrange(year, month)[1]
        start_date = datetime(year, month, 1).date()
        end_date = datetime(year, month, days_in_month).date()

        field = get_object_or_404(Field, pk=pk)

        statuses = FieldStatusHistory.objects.filter(
            field=field,
            start_date__lte=end_date,
            end_date__gte=start_date,
        )

        maintain_days = statuses.filter(status=Field.FieldStatus.MAINTENANCE).aggregate(
            total_days=Count("id")
        )["total_days"]
        booked_days = statuses.filter(status=Field.FieldStatus.BOOKED).aggregate(
            total_days=Count("id")
        )["total_days"]
        available_days = days_in_month - (maintain_days + booked_days)

        return Response(
            {
                "field_id": field.id,
                "field_name": field.name,
                "month": str(month).zfill(2),
                "year": str(year),
                "report": {
                    "available_days": available_days,
                    "maintain_days": maintain_days,
                    "booked_days": booked_days,
                },
            },
            status=status.HTTP_200_OK,
        )


@receiver(post_save, sender=Booking)
def book_field(sender, instance, **kwargs):
    if instance.paid:
        NotificationManager.create_notification(
            entity=instance,
            entity_type=EntityType.BOOKING,
            sender=instance.user,
        )
