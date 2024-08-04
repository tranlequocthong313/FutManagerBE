from django.urls import include, path
from rest_framework import routers

from .views import FieldView

r = routers.DefaultRouter()
r.register("fields", FieldView, basename="field")

urlpatterns = [
    path("", include(r.urls)),
]
