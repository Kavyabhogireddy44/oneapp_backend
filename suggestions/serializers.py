from suggestions.models import Suggestion
from rest_framework import serializers

class SuggesionSerializers(serializers.ModelSerializer):
    class Meta:
        model=Suggestion
        fields='__all__'
