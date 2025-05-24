from django.shortcuts import render
from rest_framework import generics
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from login.utils import verify_jwt

class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

# class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
# class UserByTokenAPIView(APIView):
#     def post(self, request):
#         token = request.data.get('token')
#         if not token:
#             return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
#         payload = verify_jwt(token)
#         print("payload", payload)
#         if not payload:
#             return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
#         user_id = payload.get('user_id')
#         print("user_id", user_id)
#         try:
#             user = CustomUser.objects.get(id=user_id)
#         except CustomUser.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#         serializer = UserSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
class CheckPhoneNumberAPIView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response(False, status=status.HTTP_200_OK)  # or return an error if preferred
        
        exists = CustomUser.objects.filter(phone=phone).exists()
        return Response(exists, status=status.HTTP_200_OK)
    
class UserByTokenAPIView(APIView):
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

    def post(self, request):
        """Retrieve user by token."""
        token = request.data.get('token')
        user, error = self.get_user_from_token(token)
        if error:
            return error
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """Update user by token."""
        token = request.data.get('token')
        user, error = self.get_user_from_token(token)
        if error:
            return error

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteUserByTokenAPIView(APIView):
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

        try:
            user = CustomUser.objects.get(id=user_id)
        except user.DoesNotExist:
            return Response({'error': 'user not found for this user'}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({'message': 'user deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

