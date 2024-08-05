from django.urls import include, path
from rest_framework import routers

from help.views import HelpView


r = routers.DefaultRouter()
r.register("helps", HelpView, basename="help")

urlpatterns = [
    path("", include(r.urls)),
]
