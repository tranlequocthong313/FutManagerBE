from rest_framework import serializers
from .models import Review
from user.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

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

    def get_user(self, obj):
        return UserSerializer(obj.user).data
