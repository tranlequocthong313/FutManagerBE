from django.urls import path, include
from rest_framework.routers import DefaultRouter

from review.views import RatingStatsView

router = DefaultRouter()
router.register(r"fields", RatingStatsView, basename="field")

urlpatterns = [
    path("", include(router.urls)),
]
