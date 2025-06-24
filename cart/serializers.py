from rest_framework import serializers
from .models import Cart, CartItem
from grocery.serializers import GroceryItemSerializer

class CartItemSerializer(serializers.ModelSerializer):
    item_details = GroceryItemSerializer(source='item', read_only=True)
    available = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'item', 'item_details', 'quantity', 'available', 'status']

    def get_available(self, obj):
        return obj.is_valid()

    def get_status(self, obj):
        return obj.status()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at']