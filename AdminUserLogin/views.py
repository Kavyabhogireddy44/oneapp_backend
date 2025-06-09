from django.shortcuts import render
# login/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from AdminUser.models import AdminUser

from AdminUser.serializers import AdminUserSerializer

from .utils import create_admin_jwt, verify_admin_jwt


class CreateTokenAPIView(APIView):
    def post(self, request):
        print("request.data", request.data)
        user_name = request.data.get('phone')

        if not user_name:
            return Response({'error': 'user_name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            print("request.data.get('password')", request.data.get('password'))
            user = AdminUser.objects.get(phone=user_name,password=request.data.get('password'))
            print("user", user)
            if not user.is_active:
                return Response({'error': 'User is not active.'}, status=status.HTTP_403_FORBIDDEN)
            token = create_admin_jwt(user.id,user.phone,user.role)
            return Response({'token': token}, status=status.HTTP_200_OK)
        except AdminUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

class VerifyTokenAPIView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        decoded = verify_admin_jwt(token)

        if not decoded:
            return Response({'valid': False, 'error': 'Invalid or expired token.'}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = decoded.get('user_id')
        if not user_id:
            return Response({'valid': False, 'error': 'Token does not contain user_id.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = AdminUser.objects.get(id=user_id)
        except AdminUser.DoesNotExist:
            return Response({'valid': False, 'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'valid': True, 'data': decoded}, status=status.HTTP_200_OK)
    