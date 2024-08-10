from urllib.parse import parse_qs, urlparse

from field.serializers import BookingResponseSerializer
from rest_framework import status
from rest_framework.response import Response

from payment import momo
from payment.models import Payment
from payment.vnpay import vnpay


class PaymentService:
    MOMO_SUCCESS_CODE = 0
    VNPAY_SUCCESS_CODE = "00"

    def pay(self, request, booking, payment_channel=Payment.PaymentChannel.MOMO):
        if booking is None:
            raise ValueError("request and booking are required")
        if payment_channel == Payment.PaymentChannel.MOMO:
            return self.pay_with_momo(request, booking)
        elif payment_channel == Payment.PaymentChannel.VN_PAY:
            return self.pay_with_vnpay(request, booking)
        raise ValueError("Payment channel is invalid")

    def pay_with_vnpay(self, request, booking):
        payment_url = vnpay().pay(request, booking)
        parsed_url = urlparse(payment_url)
        vnpay_reference_number = parse_qs(parsed_url.query)["vnp_TxnRef"][0]

        Payment.objects.create(
            channel=Payment.PaymentChannel.VN_PAY,
            status=Payment.PaymentStatus.PENDING,
            booking=booking,
            reference_code=vnpay_reference_number,
        )

        response_serializer = BookingResponseSerializer(
            data={"payment_url": payment_url}
        )
        if response_serializer.is_valid():
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def pay_with_momo(self, request, booking):
        r = momo.pay(request, booking)
        if not r.ok:
            return Response(
                "Internal server error", status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        data = r.json()
        if data["resultCode"] != self.MOMO_SUCCESS_CODE:
            return Response(
                "Transaction is not success", status=status.HTTP_400_BAD_REQUEST
            )

        Payment.objects.create(
            channel=Payment.PaymentChannel.MOMO,
            status=Payment.PaymentStatus.PENDING,
            booking=booking,
            reference_code=data["requestId"],
        )

        response_serializer = BookingResponseSerializer(
            data={"payment_url": data["payUrl"]}
        )
        if response_serializer.is_valid():
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
