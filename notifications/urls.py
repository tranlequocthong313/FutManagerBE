from django.urls import include, path
from rest_framework import routers

from .views import NotificationView


r = routers.DefaultRouter()
r.register("notifications", NotificationView, basename="notification")

urlpatterns = [
    path("", include(r.urls)),
]
