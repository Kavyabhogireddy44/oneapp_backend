from django.shortcuts import render
from rest_framework import generics 
from .models import MetaData
from .serializers import MetadataSerializer

class MetadataListCreateAPIView(generics.ListCreateAPIView):
    queryset = MetaData.objects.all()
    serializer_class = MetadataSerializer

class MetadataRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MetaData.objects.all()   
    serializer_class = MetadataSerializer

# Create your views here.
