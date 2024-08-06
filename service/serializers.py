from rest_framework import serializers

from service.models import Introduction, CustomerSupport


class IntroductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Introduction
        fields = ["id", "content", "version", "created_date", "updated_date"]


class CustomerSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSupport
        fields = ['id', 'service_name', 'content', "created_date", "updated_date"]
