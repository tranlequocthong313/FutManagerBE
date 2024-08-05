from rest_framework import serializers

from service.models import Introduction


class IntroductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Introduction
        fields = ["id", "content", "version", "created_date", "updated_date"]
