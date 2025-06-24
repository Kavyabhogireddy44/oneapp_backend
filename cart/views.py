from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart
from .serializers import CartSerializer
from login.utils import verify_jwt  # assuming you're using JWT
from cart.mixins import GetUserFromTokenMixin  # Adjust path as needed
from grocery.models import GroceryItem
from cart.models import CartItem

class CreateCartView(APIView, GetUserFromTokenMixin):
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        user, error = self.get_user_from_token(token)
        if error:
            return error

        # Create the cart
        cart = Cart.objects.create(user=user)

        # Get the items from the request
        items_data = request.data.get('items', [])

        # Loop and create CartItems
        for item_data in items_data:
            item_id = item_data.get('grocery_item')
            quantity = item_data.get('quantity', 1)

            try:
                grocery_item = GroceryItem.objects.get(id=item_id)

                # Check if available
                if grocery_item.is_available and grocery_item.stock >= quantity:
                    CartItem.objects.create(cart=cart, item=grocery_item, quantity=quantity)
                else:
                    return Response({
                        'error': f'Item "{grocery_item.name}" is unavailable or out of stock.'
                    }, status=status.HTTP_400_BAD_REQUEST)

            except GroceryItem.DoesNotExist:
                return Response({'error': f'Grocery item with id {item_id} not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the cart and return
        serializer = CartSerializer(cart)  # Make sure your serializer includes items
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ViewCartAPIView(APIView, GetUserFromTokenMixin):
    def post(self, request):
        token = request.data.get('token')
        user, error = self.get_user_from_token(token)
        if error:
            return error

        cart_items = Cart.objects.filter(user=user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data, status=200)
class UpdateCartItemAPIView(APIView, GetUserFromTokenMixin):
    """
    Updates quantity for a cart item.
    """
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        cart_item_id = request.data.get('cart_item_id')
        quantity = request.data.get('quantity')

        if not token or not cart_item_id or quantity is None:
            return Response(
                {'error': 'token, cart_item_id, and quantity are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user, error = self.get_user_from_token(token)
        if error:
            return error

        try:
            cart_item = Cart.objects.get(id=cart_item_id, user=user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)

        cart_item.quantity = quantity
        cart_item.save()

        serializer = CartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DeleteCartItemAPIView(APIView, GetUserFromTokenMixin):
    """
    Deletes a cart item from the user's cart.
    """
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        cart_item_id = request.data.get('cart_item_id')

        if not token or not cart_item_id:
            return Response(
                {'error': 'token and cart_item_id are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user, error = self.get_user_from_token(token)
        if error:
            return error

        try:
            cart_item = Cart.objects.get(id=cart_item_id, user=user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response({'message': 'Cart item deleted successfully.'}, status=status.HTTP_200_OK)