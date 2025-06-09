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
        try:
            user = AdminUser.objects.get(id=user_id)
            return user, None
        except AdminUser.DoesNotExist:
            return None, Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


    def post(self, request, *args, **kwargs):
    # ✅ Check if AdminUser table is empty
        if AdminUser.objects.exists():
            token = request.data.get('token')
            if not token:
                return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

            user, error = self.get_user_from_token(token)
            if error:
                return error

            # Attach user to data (optional based on use case)
            data = request.data.copy()
            data['user'] = user.id
        else:
            # ✅ No users in DB, no token needed — allow first admin creation
            data = request.data.copy()

        # 👇 Proceed to create user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


