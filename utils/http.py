from django.utils.http import urlsafe_base64_decode
from urllib.parse import urlparse


def get_client_ip(request):
    return (
        x_forwarded_for.split(",")[0]
        if (x_forwarded_for := request.META.get("HTTP_X_FORWARDED_FOR"))
        else request.META.get("REMOTE_ADDR")
    )


def get_domain_url(request):
    full_url = request.build_absolute_uri()
    parsed_url = urlparse(full_url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"
