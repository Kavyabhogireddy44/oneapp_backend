from AdminUser.models import AdminUser
from rest_framework import serializers

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'required': False},
            'is_staff': {'required': False},
        }
