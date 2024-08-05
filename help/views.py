from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated

from help.models import HelpCategory
from help.serializers import HelpCategorySerializer


# Create your views here.
class HelpView(ListAPIView, ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HelpCategorySerializer

    def get_queryset(self):
        queryset = HelpCategory.objects.all()
        if category := self.request.query_params.get("category"):
            get_object_or_404(HelpCategory, pk=category)
            queryset = queryset.filter(id=category)
        return queryset
