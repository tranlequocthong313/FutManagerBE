from rest_framework import serializers
from .models import Help, HelpCategory


class HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = ["id", "title", "content", "created_date", "updated_date"]


class HelpCategorySerializer(serializers.ModelSerializer):
    helps = HelpSerializer(many=True)

    class Meta:
        model = HelpCategory
        fields = ["id", "name", "helps"]
