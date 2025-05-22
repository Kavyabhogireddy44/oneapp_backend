from django.shortcuts import render
from address.models import Address
from address.serializers import AddressSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from login.utils import verify_jwt
from user.models import CustomUser
from rest_framework import status

class AddressListCreateAPIview(generics.ListCreateAPIView):
    serializer_class = AddressSerializer

    def get_user_from_token(self, token):
        payload = verify_jwt(token)
        print("payload",payload)
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

        address = Address.objects.filter(user=user_id)
        if not address.exists():
            return Response({'message': 'No orders found for this user'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AddressSerializer(address, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        print("token",token)
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        user, error = self.get_user_from_token(token)
        if error:
            return error

        data = request.data.copy()
        data['user'] = user.id  # attach user to the order
        data['user_name']=user.first_name
        print("data",data)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class AddressRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset=Address.objects.all()
#     serializer_class=AddressSerializer

class AddressByTokenAPIView(APIView):
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

    def post(self, request, Address_id):
        """Retrieve a specific order using POST (to allow token in body)"""
        token = request.data.get('token')
        user, error = self.get_user_from_token(token)
        if error:
            return error

        try:
            Address = Address.objects.get(id=Address_id)
        except Address.DoesNotExist:
            return Response({'error': 'Address not found for this user'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AddressSerializer(Address)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, Address_id):
        """Update order"""
        token = request.data.get('token')
        user, error = self.get_user_from_token(token)
        if error:
            return error

        try:
            Address = Address.objects.get(id=Address_id)
        except Address.DoesNotExist:
            return Response({'error': 'Order not found for this user'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AddressSerializer(Address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, Address_id):
        """Delete order"""
        token = request.data.get('token')
        user, error = self.get_user_from_token(token)
        if error:
            return error

        try:
            Address = Address.objects.get(id=Address_id)
        except Address.DoesNotExist:
            return Response({'error': 'Address not found for this user'}, status=status.HTTP_404_NOT_FOUND)

        Address.delete()
        return Response({'message': 'Address deleted successfully'}, status=status.HTTP_204_NO_CONTENT)



# Create your views here.
