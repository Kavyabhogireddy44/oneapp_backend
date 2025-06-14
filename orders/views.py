from django.shortcuts import render

from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer
from user.models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from login.utils import verify_jwt 
from datetime import datetime, timedelta
from django.utils import timezone
from collections import defaultdict
import json
# class OrderListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

# class OrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer


# class UserOrdersAPIView(APIView):
#     def get(self, request, user_id):
#         try:
#             user = CustomUser.objects.get(id=user_id)
#         except CustomUser.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#         orders = Order.objects.filter(user=user)
#         serializer = OrderSerializer(orders, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
class OrderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_user_from_token(self, token):
        payload = verify_jwt(token)
        if not payload:
            return None, Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = payload.get('user_id')
        try:
            user = CustomUser.objects.get(id=user_id)
            return user, None
        except CustomUser.DoesNotExist:
            return None, Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        token = request.data.get('token')  # Token in body
        user, error = self.get_user_from_token(token)
        if error:
            return error

        orders = Order.objects.all()
        if not orders.exists():
            return Response({'message': 'No orders found for this user'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        user, error = self.get_user_from_token(token)
        if error:
            return error

        data = request.data.copy()
        data['user'] = user.id  # attach user to the order

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserOrdersByTokenAPIView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        payload = verify_jwt(token)
        print("payload", payload)
        if not payload:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = payload.get('user_id')
        print("user_id", user_id)
        try:
            user = CustomUser.objects.get(id=user_id)
            user=user.id
            print("user", user)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        orders = Order.objects.filter(user=user)
        print("orders", orders)
        if not orders.exists():
            return Response({'message': 'No orders found for this user'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrdersByTokenAPIView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        payload = verify_jwt(token)
        print("payload", payload)
        if not payload:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = payload.get('user_id')
        print("user_id", user_id)
        try:
            user = CustomUser.objects.get(id=user_id)
            user=user.id
            print("user", user)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        orders = Order.objects.all()
        print("orders", orders)
        if not orders.exists():
            return Response({'message': 'No orders found for this user'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderByTokenAPIView(APIView):
    def get_user_from_token(self, token):
        if not token:
            return None, Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        payload = verify_jwt(token)
        if not payload:
            return None, Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = payload.get('user_id')
        try:
            user = CustomUser.objects.get(id=user_id)
            return user, None
        except CustomUser.DoesNotExist:
            return None, Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, order_id):
        """Retrieve a specific order using POST (to allow token in body)"""
        token = request.data.get('token')
        user, error = self.get_user_from_token(token)
        if error:
            return error

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found for this user'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, order_id):
        """Update order"""
        token = request.data.get('token')
        user, error = self.get_user_from_token(token)
        if error:
            return error

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found for this user'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id):
        """Delete order"""
        token = request.data.get('token')
        user, error = self.get_user_from_token(token)
        if error:
            return error

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found for this user'}, status=status.HTTP_404_NOT_FOUND)

        order.delete()
        return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# class OrderStatusAPIView(APIView):
#     def post(self, request):
#         token = request.data.get('token')
#         if not token:
#             return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
#         payload = verify_jwt(token)
#         if not payload:
#             return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
#         user_id = payload.get('user_id')
#         try:
#             user = CustomUser.objects.get(id=user_id)
#         except CustomUser.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#         orders = Order.objects.filter(user=user)
#         if not orders.exists():
#             return Response({'message': 'No orders found for this user'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = OrderSerializer(orders, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
class OrdersScheduledAPIView(APIView):
    def get(self, request):
        
        # Get today’s date
        today = datetime.now().date()

        # Filter orders for today
        orders = Order.objects.filter(created_at__date=today)
        if not orders.exists():
            return Response({'message': 'No orders found for this user today'}, status=status.HTTP_404_NOT_FOUND)

        # Dictionaries to track type counts and total cost
        type_count = defaultdict(int)
        type_cost = defaultdict(float)

        for order in orders:
            order_type = order.type.capitalize()  # Ensure consistency
            try:
                details = json.loads(order.details)
                final_cost = float(details.get('finalCost', 0))
            except Exception as e:
                final_cost = 0

            type_count[order_type] += 1
            type_cost[order_type] += final_cost

        # Convert to list format
        count_list = [[key, value] for key, value in type_count.items()]
        cost_list = [[key, value] for key, value in type_cost.items()]

        return Response([count_list, cost_list], status=status.HTTP_200_OK)