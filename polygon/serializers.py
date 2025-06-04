from rest_framework import serializers
from .models import AreaPolygon


class AreaPolygonSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaPolygon
        fields = '__all__'
