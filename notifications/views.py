from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet

from . import models, serializers


# Create your views here.
class NotificationView(ListAPIView, ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.NotificationSerializer

    def get_queryset(self):
        queryset = models.Notification.objects.filter(
            user=self.request.user,
        )
        return queryset.order_by("-id")
