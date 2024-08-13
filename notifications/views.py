from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from firebase import topic

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

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data["badge"] = models.Notification.objects.filter(read=False).count()
        return response

    @action(
        detail=False,
        methods=["POST"],
        serializer_class=serializers.ReadNotificationSerializer,
    )
    def read(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if notification := (
            self.get_queryset()
            .filter(
                notification_content_id=int(
                    serializer.validated_data["notification_content_id"]
                )
            )
            .first()
        ):
            notification.read = True
            notification.save()
            return Response(
                {"status": 200, "message": "Read successfully"}, status.HTTP_200_OK
            )
        return Response(
            {"status": 400, "message": "Read failed"}, status.HTTP_400_BAD_REQUEST
        )


class FCMTokenView(CreateAPIView, DestroyAPIView, ViewSet):
    queryset = models.FCMToken.objects.all()
    serializer_class = serializers.FCMTokenSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            fcm_token, created = serializer.save(user=request.user)
            if request.user.is_staff:
                topic.subscribe_to_topic(fcm_tokens=fcm_token.token, topic="admin")
            else:
                topic.subscribe_to_topic(fcm_tokens=fcm_token.token, topic="customer")
            return Response(
                serializers.FCMTokenSerializer(fcm_token).data, status.HTTP_201_CREATED
            )
        except Exception:
            return Response(
                "Internal server error :(", status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        topic.unsubscribe_from_topic(
            fcm_tokens=instance.token,
            topic="admin" if instance.user.is_staff else "customer",
        )
        return super().destroy(request, *args, **kwargs)
