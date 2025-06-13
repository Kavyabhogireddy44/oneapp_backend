from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from books.models import Service
from books.serializers import ServiceSerializer

# class ServiceListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer

#     def create(self, request, *args, **kwargs):
#         is_bulk = isinstance(request.data, list)
#         serializer = self.get_serializer(data=request.data, many=is_bulk)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

from rest_framework import generics, status
from rest_framework.response import Response
from .models import Service
from .serializers import ServiceSerializer

class ServiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def create(self, request, *args, **kwargs):
        is_bulk = isinstance(request.data, list)

        # Log incoming data (optional for debugging)
        print("Incoming data:", request.data)

        serializer = self.get_serializer(data=request.data, many=is_bulk)

        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        except Exception as e:
            print("Error during creation:", str(e))  # Optional
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ActiveServiceListAPIView(generics.ListAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return Service.objects.filter(status="active")
    
    
class ServiceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServicesCountAPIView(APIView):
    def get(self, request, *args, **kwargs):
        active_count = Service.objects.filter(status="active").count()
        inactive_count = Service.objects.filter(status="inactive").count()
        coming_soon_count = Service.objects.filter(status="coming_soon").count()
        return Response([
            ["Available", active_count],
            ["Inactive", inactive_count],
            ["Coming Soon", coming_soon_count]
        ], status=status.HTTP_200_OK)
