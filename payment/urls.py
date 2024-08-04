from django.urls import include, path
from rest_framework import routers

from payment.views import PaymentView


r = routers.DefaultRouter()
r.register("payments", PaymentView, basename="payment")

urlpatterns = [
    path("", include(r.urls)),
]
