from rest_framework import serializers
from .models import Polygon


class AreaPolygonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polygon
        fields = '__all__'
