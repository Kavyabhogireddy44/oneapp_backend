from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart
from .serializers import CartSerializer,CartItemSerializer
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
        # cart = Cart.objects.create(user=user)
        cart, created = Cart.objects.get_or_create(user=user)

        serializer = CartSerializer(cart)  # Ensure CartSerializer includes related CartItems
        return Response(serializer.data, status=status.HTTP_200_OK)




class ViewCartAPIView(APIView, GetUserFromTokenMixin):
    def post(self, request):
        token = request.data.get('token')
        user, error = self.get_user_from_token(token)
        if error:
            return error

        carts = Cart.objects.filter(user=user)

        # Filter cart items in memory
        filtered_data = []
        for cart in carts:
            items = cart.items.filter(quantity__gt=0)
            if items.exists():
                cart_data = CartSerializer(cart).data
                cart_data['items'] = CartItemSerializer(items, many=True).data
                filtered_data.append(cart_data)

        return Response(filtered_data, status=200)
# class UpdateCartItemAPIView(APIView, GetUserFromTokenMixin):
#     """
#     Updates quantity for a cart item.
#     """
#     def post(self, request, *args, **kwargs):
#         token = request.data.get('token')
#         if not token:
#             return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

#         user, error = self.get_user_from_token(token)
#         if error:
#             return error

#         # Get or create cart
#         cart, _ = Cart.objects.get_or_create(user=user)

#         items_data = request.data.get('items', [])
#         for item_data in items_data:
#             cart_item_id = item_data.get("id")
#             grocery_id = item_data.get("item")
#             quantity = item_data.get("quantity", 1)

#             try:
#                 grocery_item = GroceryItem.objects.get(id=grocery_id)
#             except GroceryItem.DoesNotExist:
#                 return Response({'error': f"Grocery item {grocery_id} not found"}, status=404)

#             if cart_item_id:
#                 try:
#                     cart_item = CartItem.objects.get(id=cart_item_id, cart=cart, item=grocery_item)
#                     cart_item.quantity = quantity
#                     cart_item.save()
#                 except CartItem.DoesNotExist:
#                     return Response({'error': f"Cart item with ID {cart_item_id} not found for this user."}, status=404)
#             else:
#                 # Check if item already exists in cart for safety
#                 existing = CartItem.objects.filter(cart=cart, item=grocery_item).first()
#                 if existing:
#                     existing.quantity = quantity
#                     existing.save()
#                 else:
#                     CartItem.objects.create(cart=cart, item=grocery_item, quantity=quantity)

#         serializer = CartSerializer(cart)
#         return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateCartItemAPIView(APIView, GetUserFromTokenMixin):
    """
    Updates quantity for a cart item.
    """
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        user, error = self.get_user_from_token(token)
        if error:
            return error

        # Get or create cart
        cart, _ = Cart.objects.get_or_create(user=user)

        items_data = request.data.get('items', [])
        for item_data in items_data:
            cart_item_id = item_data.get("id")
            grocery_id = item_data.get("item")
            quantity = item_data.get("quantity", 1)

            try:
                grocery_item = GroceryItem.objects.get(id=grocery_id)
            except GroceryItem.DoesNotExist:
                return Response({'error': f"Grocery item {grocery_id} not found"}, status=404)

            if cart_item_id:
                try:
                    cart_item = CartItem.objects.get(id=cart_item_id, cart=cart, item=grocery_item)
                    cart_item.quantity = quantity
                    cart_item.save()
                except CartItem.DoesNotExist:
                    return Response({'error': f"Cart item with ID {cart_item_id} not found for this user."}, status=404)
            else:
                # Check if item already exists in cart for safety
                existing = CartItem.objects.filter(cart=cart, item=grocery_item).first()
                if existing:
                    existing.quantity = quantity
                    existing.save()
                else:
                    CartItem.objects.create(cart=cart, item=grocery_item, quantity=quantity)

        serializer = CartSerializer(cart)
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

class FinalizeCartAfterPaymentAPIView(APIView, GetUserFromTokenMixin):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        user, error = self.get_user_from_token(token)
        if error:
            return error

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update stock and validate
        for cart_item in cart.items.all():
            item = cart_item.item
            if item.stock >= cart_item.quantity:
                item.stock -= cart_item.quantity
                item.save()
            else:
                return Response({
                    'error': f'Not enough stock for "{item.name}". Available: {item.stock}, Requested: {cart_item.quantity}'
                }, status=status.HTTP_400_BAD_REQUEST)

        # Optionally clear cart after purchase
        cart.items.all().delete()

        return Response({'message': 'Purchase successful, stock updated.'}, status=status.HTTP_200_OK)