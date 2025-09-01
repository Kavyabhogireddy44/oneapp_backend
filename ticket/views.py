from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from ticket.models import Ticket    
from ticket.serializers import TicketSerializer
from rest_framework.response import Response
from user.models import CustomUser
from rest_framework.views import APIView
from login.utils import verify_jwt
from AdminUserLogin.utils import  verify_admin_jwt
from AdminUser.models import AdminUser

class TicketUserListAPIView(APIView):
    #i have topost method because token is in body 
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        payload = verify_jwt(token)
        if not payload:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = payload.get('user_id')
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        tickets = Ticket.objects.filter(user=user)
        if not tickets.exists():
            return Response({'message': 'No tickets found for this user'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
             
    
class TicketUserCreateAPIView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        payload = verify_jwt(token)
        if not payload:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = payload.get('user_id')
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['user'] = user.id  # attach user to the ticket
        data['user_name']=user.first_name

        serializer = TicketSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#now admin can see all tickets and he can created updated  deletegive diff urls by authentication

class TicketAdminListAPIView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        payload = verify_admin_jwt(token)
        if not payload:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = payload.get('Admin_user_id')

        try:
            user = AdminUser.objects.get(id=user_id)
            if user.role != 'admin':
                return Response({'error': 'Only admin can access all tickets'}, status=status.HTTP_403_FORBIDDEN)
        except AdminUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TicketAdminDeleteAPIView(APIView):
    def post(self, request, ticket_id):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        payload = verify_admin_jwt(token)
        if not payload:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = payload.get('Admin_user_id')
        try:
            user = AdminUser.objects.get(id=user_id)
            if user.role != 'admin':
                return Response({'error': 'Only admin can delete tickets'}, status=status.HTTP_403_FORBIDDEN)
        except AdminUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.delete()
            return Response({'message': 'Ticket deleted successfully'}, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
    
class TicketAdminUpdateAPIView(APIView):
    def post(self, request, ticket_id):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        payload = verify_admin_jwt(token)
        if not payload:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = payload.get('Admin_user_id')
        try:
            user = AdminUser.objects.get(id=user_id)
            if user.role != 'admin':
                return Response({'error': 'Only admin can update tickets'}, status=status.HTTP_403_FORBIDDEN)
        except AdminUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TicketSerializer(ticket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TicketAdmincreateadminAPIView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        payload = verify_admin_jwt(token)
        if not payload:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = payload.get('Admin_user_id')
        try:
            user = AdminUser.objects.get(id=user_id)
            if user.role != 'admin':
                return Response({'error': 'Only admin can create tickets'}, status=status.HTTP_403_FORBIDDEN)
        except AdminUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        # Admin can create ticket for any user, so user field must be provided in request
        user_id = data.get('user')
        if not user_id:
            return Response({'error': 'User ID is required to create a ticket'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ticket_user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        data['user_name']=ticket_user.first_name

        serializer = TicketSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 









