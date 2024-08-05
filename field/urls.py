from django.urls import include, path
from rest_framework import routers

from review.views import RatingView

from .views import FieldView

router = routers.DefaultRouter()
router.register(r"fields", FieldView, basename="field")

rating_list = RatingView.as_view({"get": "list", "post": "create"})

urlpatterns = [
    path("", include(router.urls)),
    path("fields/<int:field_pk>/ratings/", rating_list, name="field-ratings"),
]
