from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import Polygon
from .serializers import AreaPolygonSerializer

class AreaPolygonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Polygon.objects.all()
    serializer_class = AreaPolygonSerializer
class AreaPolygonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset =Polygon.objects.all()
    serializer_class = AreaPolygonSerializer


# Create your views here.
