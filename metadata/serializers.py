from rest_framework import serializers
from .models import MetaData

class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaData
        fields = '__all__'