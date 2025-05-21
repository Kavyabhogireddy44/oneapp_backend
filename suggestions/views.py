from django.shortcuts import render
from rest_framework import generics
from suggestions.models import Suggestion
from suggestions.serializers import SuggesionSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from login.utils import verify_jwt
from user.models import CustomUser



# Create your views here.
