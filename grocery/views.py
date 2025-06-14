from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework import status

from .models import GroceryItem
from .serializers import GroceryItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from AdminUser.models import AdminUser


from AdminUserLogin.utils import  verify_admin_jwt


class GroceryCreateAPIView(GenericAPIView):
    serializer_class = GroceryItemSerializer

    def get_user_from_token(self, token):
        payload = verify_admin_jwt(token)
        if not payload:
            return None, Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = payload.get('user_id')
        try:
            user = AdminUser.objects.get(id=user_id)
            return user, None
        except AdminUser.DoesNotExist:
            return None, Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        user, error = self.get_user_from_token(token)
        if error:
            return error

        data = request.data.copy()
        data['user'] = user.id  # attach user to the order

        serializer = self.get_serializer(data=data) #give explanation through this line
        print("serializer", serializer)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class GroceryListAPIView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        payload = verify_admin_jwt(token)
        print("payload", payload)
        if not payload:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = payload.get('user_id')
        role_id = payload.get('role')
        print("user_id", user_id)
        try:
            user = AdminUser.objects.get(id=user_id) 
            user=user.id
            print("user", user)
        except AdminUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        grocerylist = GroceryItem.objects.all()
        if not grocerylist.exists():
            return Response({'message': 'groceryitem not found for this user'}, status=status.HTTP_404_NOT_FOUND)

        serializer = GroceryItemSerializer(grocerylist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  
    
class GroceryDetailAPIView(APIView):
    def get_user_from_token(self, token):
        payload = verify_admin_jwt(token)
        if not payload:
            return None, Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        user_id= payload.get('user_id')
        role_id = payload.get('role')
        print("role_id", role_id)
        try:
            user = AdminUser.objects.get(role=role_id,id=user_id)
            print("user", user)
            return user, None
        except AdminUser.DoesNotExist:
            return None, Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request,pk):
        token = request.data.get('token')
        user, error = self.get_user_from_token(token)
        print("user", user)
        role_id = user.role
        user_id = user.id
        print("user_id", user_id)
        if error:
            return error
        try:
            grocery = GroceryItem.objects.get(id=pk)#pk= event_id
        except grocery.DoesNotExist:
            return Response({'error': 'groceryitem not found for this user'}, status=status.HTTP_404_NOT_FOUND)
        role_id = user.role
        print("role_id", role_id)
        print("type(role_id)", type(role_id))

        serializer = GroceryItemSerializer(grocery, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class GroceryDeleteAPIView(APIView):
    def post(self, request, pk):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        payload = verify_admin_jwt(token)
        if not payload:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = payload.get('user_id')
        role_id = payload.get('role')
        try:
            user = AdminUser.objects.get(id=user_id)
        except AdminUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            grocery = GroceryItem.objects.get(id=pk)
            grocery.delete()
            return Response({'message': 'groceryitem deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except AdminUser.DoesNotExist:
            return Response({'error': 'item not found'}, status=status.HTTP_404_NOT_FOUND)


