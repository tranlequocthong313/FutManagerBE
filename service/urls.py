from django.urls import include, path
from rest_framework import routers

from service.views import IntroductionView, CustomerSupportView


r = routers.DefaultRouter()
r.register("abouts", IntroductionView, basename="about")
r.register("supports", CustomerSupportView, basename="support")

urlpatterns = [
    path("", include(r.urls)),
]
