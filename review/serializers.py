from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "rating",
            "review",
            "user",
            "field",
            "created_date",
            "updated_date",
        ]
        read_only_fields = ["id", "user", "field", "created_date", "updated_date"]
