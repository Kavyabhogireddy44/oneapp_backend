from suggestions.models import Suggestion
from rest_framework import serializers

class SuggesionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Suggestion
        fields='__all__'
        extra_kwargs = {
            'status': {'required': False},  
            'user_name': {'required': False},
            'status': {'required': False},
        }
