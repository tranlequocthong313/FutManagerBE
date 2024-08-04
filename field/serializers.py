from payment.models import Payment
from rest_framework import serializers

from field.models import Booking, Field


class FieldSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["img"] = instance.img_url
        rep["avg_rating"] = instance.avg_rating
        return rep

    class Meta:
        model = Field
        fields = ["id", "name", "img", "price", "status", "field_type", "avg_rating"]


class BookingSerializer(serializers.ModelSerializer):
    booking_date = serializers.DateField(format="%Y-%m-%d")
    from_time = serializers.TimeField(format="%H:%M")
    to_time = serializers.TimeField(format="%H:%M")
    payment_channel = serializers.ChoiceField(choices=Payment.PaymentChannel.choices)

    class Meta:
        model = Booking
        fields = [
            "booking_date",
            "from_time",
            "to_time",
            "note",
            "booker_name",
            "phone_number",
            "payment_channel",
        ]

    def create(self, validated_data):
        validated_data.pop("payment_channel")
        return Booking.objects.create(**validated_data)


class BookingResponseSerializer(serializers.Serializer):
    payment_url = serializers.CharField()


class BookingListSerializer(serializers.ModelSerializer):
    booking_date = serializers.DateField()
    from_time = serializers.TimeField()
    to_time = serializers.TimeField()

    class Meta:
        model = Booking
        fields = [
            "id",
            "field",
            "booking_date",
            "from_time",
            "to_time",
            "paid",
            "created_date",
            "updated_date",
        ]
