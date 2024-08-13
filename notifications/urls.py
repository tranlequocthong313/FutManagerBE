from django.urls import include, path
from rest_framework import routers

from .views import NotificationView, FCMTokenView


r = routers.DefaultRouter()
r.register("notifications", NotificationView, basename="notification")
r.register("fcm-tokens", FCMTokenView, basename="fcm-token")

urlpatterns = [
    path("", include(r.urls)),
]
