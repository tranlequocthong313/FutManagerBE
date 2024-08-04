from rest_framework import serializers

from field.models import Field


class FieldSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["img"] = instance.img_url
        rep["avg_rating"] = instance.avg_rating
        return rep

    class Meta:
        model = Field
        fields = ["id", "name", "img", "price", "status", "field_type", "avg_rating"]
