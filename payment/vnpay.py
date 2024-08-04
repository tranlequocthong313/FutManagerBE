import hashlib
from datetime import datetime
import hmac
import urllib.parse
import uuid

from utils.http import get_client_ip, get_domain_url
from app import settings


class vnpay:
    requestData = {}
    responseData = {}

    def get_payment_url(self, vnpay_payment_url, secret_key):
        inputData = sorted(self.requestData.items())
        queryString = ""
        seq = 0
        for key, val in inputData:
            if seq == 1:
                queryString = f"{queryString}&{key}={urllib.parse.quote_plus(str(val))}"
            else:
                seq = 1
                queryString = f"{key}={urllib.parse.quote_plus(str(val))}"

        hashValue = self.__hmacsha512(secret_key, queryString)
        return f"{vnpay_payment_url}?{queryString}&vnp_SecureHash={hashValue}"

    def validate_response(self, secret_key):
        vnp_SecureHash = self.responseData["vnp_SecureHash"]
        if "vnp_SecureHash" in self.responseData.keys():
            self.responseData.pop("vnp_SecureHash")

        if "vnp_SecureHashType" in self.responseData.keys():
            self.responseData.pop("vnp_SecureHashType")

        inputData = sorted(self.responseData.items())
        seq = 0
        hasData = ""
        for key, val in inputData:
            if str(key).startswith("vnp_"):
                if seq == 1:
                    hasData = (
                        f"{hasData}&{str(key)}={urllib.parse.quote_plus(str(val))}"
                    )
                else:
                    seq = 1
                    hasData = f"{str(key)}={urllib.parse.quote_plus(str(val))}"
        hashValue = self.__hmacsha512(secret_key, hasData)

        return vnp_SecureHash == hashValue

    @staticmethod
    def __hmacsha512(key, data):
        byteKey = key.encode("utf-8")
        byteData = data.encode("utf-8")
        return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()

    def pay(self, request, booking):
        order_type = "billpayment"
        order_id = f"{booking.pk}-{str(uuid.uuid4())}"
        amount = int(booking.total_amount)
        order_desc = f"{booking.booker_name.__str__()} thanh toán tiền đặt sân {booking.field.name.__str__()}"
        language = "vn"
        ipaddr = get_client_ip(request)

        self.requestData["vnp_Version"] = "2.1.0"
        self.requestData["vnp_Command"] = "pay"
        self.requestData["vnp_TmnCode"] = settings.VNPAY_TMN_CODE
        self.requestData["vnp_Amount"] = amount * 100
        self.requestData["vnp_CurrCode"] = "VND"
        self.requestData["vnp_TxnRef"] = order_id
        self.requestData["vnp_OrderInfo"] = order_desc
        self.requestData["vnp_OrderType"] = order_type
        self.requestData["vnp_Locale"] = language
        self.requestData["vnp_CreateDate"] = datetime.now().strftime("%Y%m%d%H%M%S")
        self.requestData["vnp_IpAddr"] = ipaddr
        self.requestData["vnp_ReturnUrl"] = (
            get_domain_url(request) + settings.VNPAY_RETURN_URL
        )
        return self.get_payment_url(
            settings.VNPAY_PAYMENT_URL,
            settings.VNPAY_HASH_SECRET_KEY,
        )
