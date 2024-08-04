from django.db.models import Avg
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated

from field.models import Field
from field.serializers import FieldSerializer


# Create your views here.
class FieldView(ListAPIView, ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FieldSerializer

    # - type: Loại sân (ví dụ: sân 5, sân 7)
    # - status: Trạng thái sân (ví dụ: Có sẵn, Đã được đặt, Bảo trì)
    # - toprice: Giá tối đa (ví dụ: 300000)
    # - fromrating: Đánh giá (ví du: 1, 3, 5)
    def get_queryset(self):
        queryset = Field.objects.all()

        if type := self.request.query_params.get("type"):
            queryset = queryset.filter(field_type=type)
        if status := self.request.query_params.get("status"):
            queryset = queryset.filter(status=status)
        if from_price := self.request.query_params.get("fromprice"):
            queryset = queryset.filter(price__gte=from_price)
        if to_price := self.request.query_params.get("toprice"):
            queryset = queryset.filter(price__lte=to_price)
        if from_rating := self.request.query_params.get("fromrating"):
            queryset = queryset.annotate(rating=Avg("review__rating")).filter(
                rating__gte=from_rating
            )

        return queryset
