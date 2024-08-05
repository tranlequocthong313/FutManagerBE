from django.urls import include, path
from rest_framework import routers

from service.views import IntroductionView


r = routers.DefaultRouter()
r.register("abouts", IntroductionView, basename="about")

urlpatterns = [
    path("", include(r.urls)),
]
