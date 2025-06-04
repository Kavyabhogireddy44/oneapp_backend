from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import AreaPolygon
from .serializers import AreaPolygonSerializer

class AreaPolygonListCreateAPIView(generics.ListCreateAPIView):
    queryset = AreaPolygon.objects.all()
    serializer_class = AreaPolygonSerializer
class AreaPolygonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AreaPolygon.objects.all()
    serializer_class = AreaPolygonSerializer


# Create your views here.
