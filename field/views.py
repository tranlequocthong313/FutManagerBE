from datetime import datetime

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils import timezone
from payment.services import PaymentService
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from user.models import User

from field.models import Booking, Field
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
