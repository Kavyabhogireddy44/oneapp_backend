from django.shortcuts import render
from rest_framework import generics
from .models import Favourite
from .serializers import FavouriteSerializer

class FavouriteListCreateAPIView(generics.ListCreateAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer

class FavouriteRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
