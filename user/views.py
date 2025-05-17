from django.shortcuts import render
from rest_framework import generics
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class CheckPhoneNumberAPIView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response(False, status=status.HTTP_200_OK)  # or return an error if preferred
        
        exists = CustomUser.objects.filter(phone=phone).exists()
        return Response(exists, status=status.HTTP_200_OK)
