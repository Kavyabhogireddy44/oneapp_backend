from django.shortcuts import render
# login/views.py
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from AdminUser.models import AdminUser

from AdminUser.serializers import AdminUserSerializer

from AdminUserLogin.utils import  verify_admin_jwt


class AdminCreateAPIView(GenericAPIView):
    serializer_class = AdminUserSerializer

    def get_user_from_token(self, token):
        payload = verify_admin_jwt(token)
        if not payload:
            return None, Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = payload.get('user_id')
        role_id = payload.get('role')
        print("role_id", role_id)
        try:
            user = AdminUser.objects.get(id=user_id)
            return user, None
        except AdminUser.DoesNotExist:
            return None, Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


    def post(self, request, *args, **kwargs):
    # ✅ Check if AdminUser table is empty
        if AdminUser.objects.exists():
            token = request.data.get('token')
            role_id = request.data.get('role')
            if not token:
                return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

            user, error = self.get_user_from_token(token)
            role_id = user.role
            if error:
                return error

            # Attach user to data (optional based on use case)
            data = request.data.copy()
            data['user'] = user.id
        else:
            # ✅ No users in DB, no token needed — allow first admin creation
            data = request.data.copy()

        # 👇 Proceed to create user
        if role_id == role_id.lower():
            print("role_id", type(role_id))
            if role_id != 'admin':
                return Response({'error': 'Only admin can create other users'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=data)
        print("serializer34", serializer)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print("serializer", serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class AdminListAPIView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        payload = verify_admin_jwt(token)
        print("payload", payload)
        if not payload:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = payload.get('Admin_user_id')
        role_id = payload.get('role')
        print("user_id", user_id)
        try:
            user = AdminUser.objects.get(id=user_id) 
            user=user.id
            print("user", user)
        except AdminUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        Admin_all = AdminUser.objects.all()
        if not Admin_all.exists():
            return Response({'message': 'User not found for this user'}, status=status.HTTP_404_NOT_FOUND)
        if role_id.lower() != 'admin':
            return Response({'error': 'You Dont have Permission to View'}, status=status.HTTP_403_FORBIDDEN)    
        else:
            serializer = AdminUserSerializer(Admin_all, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)  
    
class AdminDetailAPIView(APIView):
    def get_user_from_token(self, token):
        payload = verify_admin_jwt(token)
        if not payload:
            return None, Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        user_id= payload.get('Admin_user_id')
        role_id = payload.get('role')
        print("role_id", role_id)
        try:
            user = AdminUser.objects.get(role=role_id,id=user_id)
            print("user", user)
            return user, None
        except AdminUser.DoesNotExist:
            return None, Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request,pk):
        """Update user by token."""
        token = request.data.get('token')
        user, error = self.get_user_from_token(token)
        print("user", user)
        role_id = user.role
        user_id = user.id
        print("user_id", user_id)
        if error:
            return error
        try:
            Admin_all = AdminUser.objects.get(id=pk)#pk= event_id
        except Admin_all.DoesNotExist:
            return Response({'error': 'Admin not found for this user'}, status=status.HTTP_404_NOT_FOUND)
        role_id = user.role
        print("role_id", role_id)
        print("type(role_id)", type(role_id))
        if role_id.lower() != 'admin' and str(user_id) != str(pk):
            return Response({'error': 'You Dont have Permission to Modify'}, status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = AdminUserSerializer(Admin_all, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class AdminDeleteAPIView(APIView):
    def post(self, request, pk):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        payload = verify_admin_jwt(token)
        if not payload:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = payload.get('Admin_user_id')
        role_id = payload.get('role')
        try:
            user = AdminUser.objects.get(id=user_id)
        except AdminUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            event = AdminUser.objects.get(id=pk)
            if role_id.lower() == 'admin':
                event.delete()
                return Response({'message': 'user deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'You don\'t have permission to delete'}, status=status.HTTP_403_FORBIDDEN)
        except AdminUser.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        
# I need to get a details of particular admin user - 
class AdminUserDetailAPIView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        print("token", token)
        print("request.data", request.data)
        payload = verify_admin_jwt(token)
        print("payload", payload)
        if not payload:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = payload.get('Admin_user_id')
        print("user_id", user_id)
        user = AdminUser.objects.get(id=user_id) 
        serializer = AdminUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK) 
      

 


       

      



