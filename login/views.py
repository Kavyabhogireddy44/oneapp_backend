from django.shortcuts import render
# login/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import CustomUser
from .utils import create_jwt, verify_jwt

class CreateTokenAPIView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response({'error': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(phone=phone)
            print("user",user)
            token = create_jwt(user.id, user.phone,user.first_name,user.role)
            return Response({'token': token}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

class VerifyTokenAPIView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        decoded = verify_jwt(token)

        if not decoded:
            return Response({'valid': False, 'error': 'Invalid or expired token.'}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = decoded.get('user_id')
        if not user_id:
            return Response({'valid': False, 'error': 'Token does not contain user_id.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'valid': False, 'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'valid': True, 'data': decoded}, status=status.HTTP_200_OK)

