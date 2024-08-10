import hashlib
import hmac
import uuid

import requests
from app import settings
from utils.http import get_domain_url


def pay(request, booking):
    if not booking:
        raise ValueError("invoice must not be null")
    request_id = str(uuid.uuid4())
    order_id = f"{booking.pk}-{request_id}"
    order_info = f"{booking.booker_name.__str__()} thanh toán tiền đặt sân {booking.field.name.__str__()}"
    amount = str(int(booking.total_amount))
    raw_signature = (
        f"accessKey={settings.MOMO_ACCESS_KEY}&amount={amount}&extraData=&ipnUrl={get_domain_url(request) + settings.MOMO_IPN_URL}&orderId={order_id}"
        + "&orderInfo="
        + order_info
        + "&partnerCode="
        + settings.MOMO_PARTNER_CODE
        + "&redirectUrl="
        + get_domain_url(request)
        + settings.MOMO_REDIRECT_URL
        + "&requestId="
        + request_id
        + "&requestType="
        + settings.MOMO_REQUEST_TYPE
    )
    h = hmac.new(
        bytes(settings.MOMO_SECRET_KEY, "utf8"),
        bytes(raw_signature, "utf8"),
        hashlib.sha256,
    )
    signature = h.hexdigest()
    data = {
        "partnerCode": settings.MOMO_PARTNER_CODE,
        "partnerName": settings.MOMO_PARTNER_NAME,
        "storeId": settings.MOMO_STORE_ID,
        "requestId": request_id,
        "amount": amount,
        "orderId": order_id,
        "orderInfo": order_info,
        "redirectUrl": get_domain_url(request) + settings.MOMO_REDIRECT_URL,
        "ipnUrl": get_domain_url(request) + settings.MOMO_IPN_URL,
        "lang": settings.MOMO_LANG,
        "extraData": "",
        "requestType": settings.MOMO_REQUEST_TYPE,
        "signature": signature,
    }
    return requests.post(settings.MOMO_ENDPOINT, json=data)
