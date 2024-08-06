from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet

from service.serializers import IntroductionSerializer, CustomerSupportSerializer

from .models import Introduction, CustomerSupport


# Create your views here.
class IntroductionView(ListAPIView, ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = IntroductionSerializer

    def get_queryset(self):
        queryset = Introduction.objects.all()

        if version := self.request.query_params.get("version"):
            get_object_or_404(Introduction, version=version)
            queryset = queryset.filter(version=version)

        return queryset


class CustomerSupportView(ListAPIView, ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSupportSerializer

    def get_queryset(self):
        queryset = CustomerSupport.objects.all().order_by('service_name')

        return queryset
