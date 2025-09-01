from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from ticket.models import Ticket    
from ticket.serializers import TicketSerializer
from rest_framework.response import Response
from user.models import CustomUser
from rest_framework.views import APIView
from login.utils import verify_jwt

