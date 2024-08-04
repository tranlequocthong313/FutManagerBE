from app import settings
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from payment.models import Payment
from payment.vnpay import vnpay


# Create your views here.
class PaymentView(ViewSet):
    MOMO_SUCCESS_CODE = 0
    VNPAY_SUCCESS_CODE = "00"

    @action(
        methods=["GET"],
        url_path="vnpay",
        detail=False,
        permission_classes=[AllowAny],
    )
    def return_vnpay(self, request):
        vnp = vnpay()
        vnp.responseData = request.GET.dict()
        order_id = vnp.responseData["vnp_TxnRef"]
        vnp_ResponseCode = vnp.responseData["vnp_ResponseCode"]
        if (
            vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY)
            or vnp_ResponseCode != self.VNPAY_SUCCESS_CODE
        ):
            return Response(
                "Transaction is not success", status=status.HTTP_400_BAD_REQUEST
            )

        if payment := Payment.objects.filter(reference_code=order_id):
            return (
                Response("Paid successfully", status.HTTP_200_OK)
                if payment.pay()
                else Response(
                    "Internal server error",
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            )
        else:
            return Response("Not found transaction", status=status.HTTP_404_NOT_FOUND)

    @action(
        methods=["POST"],
        url_path="ipn-momo",
        detail=False,
        permission_classes=[AllowAny],
    )
    def ipn_momo(self, request):
        if (
            "resultCode" not in request.data
            or request.data["resultCode"] != self.MOMO_SUCCESS_CODE
        ):
            return Response(
                "Transaction is not success", status=status.HTTP_400_BAD_REQUEST
            )
        payment = Payment.objects.filter(
            reference_code=request.data["requestId"]
        ).first()
        if not payment:
            return Response("Not found transaction", status=status.HTTP_404_NOT_FOUND)
        if payment.booking.total_amount != int(request.data["amount"]):
            return Response(
                "Redirected data is invalid", status=status.HTTP_400_BAD_REQUEST
            )
        if not payment.pay(transaction_id=request.data["transId"]):
            return Response(
                "Internal server error", status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(status.HTTP_204_NO_CONTENT)

    @action(
        methods=["GET"],
        url_path="momo",
        detail=False,
        permission_classes=[AllowAny],
    )
    def return_momo(self, request):
        if "resultCode" not in request.GET or request.GET.get("resultCode") != str(
            self.MOMO_SUCCESS_CODE
        ):
            return Response("Bad request", status=status.HTTP_400_BAD_REQUEST)
        if payment := Payment.objects.filter(
            reference_code=request.GET.get("requestId")
        ).first():
            return (
                Response(
                    "Redirected data is invalid",
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
                if payment.booking.total_amount != int(request.GET.get("amount"))
                else Response("Paid with Momo successfully", status.HTTP_200_OK)
            )
        else:
            return Response("Not found transaction", status=status.HTTP_400_BAD_REQUEST)
