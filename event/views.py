from django.shortcuts import render
from rest_framework import generics
from .models import Event
from AdminUser.models import AdminUser
from .serializers import EventSerializer
from user.models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from AdminUserLogin.utils import create_admin_jwt, verify_admin_jwt
from login.utils import verify_jwt

class EventListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    def get_user_from_token(self, token):
        payload = verify_admin_jwt(token)
        print("payload", payload)
        if not payload:
            return None, Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        user_id= payload.get('user_id')
        role_id = payload.get('role')
        print("role_id", role_id)
        try:
            user = AdminUser.objects.get(role=role_id,id=user_id)
            print("user", user)
            return user, None
        except AdminUser.DoesNotExist:
            return None, Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        token = request.data.get('token')  # Token in body
        user, error = self.get_user_from_token(token)
        if error:
            return error

        events = Event.objects.all()
        if not events.exists():
            return Response({'message': 'No orders found for this user'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EventSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        user, error = self.get_user_from_token(token)
        if error:
            return error

        data = request.data.copy()
        print("data", data)
        data['role'] = user.role  # attach user to the order

        serializer = self.get_serializer(data=data)
        print("serializer", serializer)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class EventsByTokenAPIView(APIView):
    serializer_class = EventSerializer
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        payload = verify_jwt(token)
        print("payload", payload)
        if not payload:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = payload.get('user_id')
        print("user_id", user_id)
        try:
            user = AdminUser.objects.get(id=user_id)
            user=user.id
            print("user", user)
        except AdminUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        events = Event.objects.filter(user=user)
        print("orders", events)
        if not events.exists():
            return Response({'message': 'No orders found for this user'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class EventsListByTokenAPIView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        payload = verify_jwt(token)
        print("payload", payload)
        if not payload:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = payload.get('user_id')
        print("user_id", user_id)
        try:
            user = CustomUser.objects.get(id=user_id) or AdminUser.objects.get(id=user_id)
            user=user.id
            print("user", user)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        events = Event.objects.all()
        if not events.exists():
            return Response({'message': 'Events found for this user'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class EventRetrieveUpdateAPIView(APIView):
    def get_user_from_token(self, token):
        payload = verify_jwt(token)
        if not payload:
            return None, Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        user_id= payload.get('user_id')
        role_id = payload.get('role')
        print("role_id", role_id)
        try:
            user = AdminUser.objects.get(role=role_id,id=user_id)
            print("user", user)
            return user, None
        except AdminUser.DoesNotExist:
            return None, Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request,pk):
        """Update user by token."""
        token = request.data.get('token')
        user, error = self.get_user_from_token(token)
        
        if error:
            return error
        try:
            event = Event.objects.get(id=pk) #pk= event_id
            print("event", event)
        except Event.DoesNotExist:
            return Response({'error': 'evens not found for this user'}, status=status.HTTP_404_NOT_FOUND)
        role_id = user.role
        print("role_id", role_id)
        print("type(role_id)", type(role_id))
        if role_id.lower() != 'admin':
            return Response({'error': 'You Dont have Permission to Modify'}, status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = EventSerializer(event, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




class DeleteEventsByTokenAPIView(APIView):
    def post(self, request, pk):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        payload = verify_jwt(token)
        if not payload:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = payload.get('user_id')
        try:
            user = AdminUser.objects.get(id=user_id)
        except AdminUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            event = Event.objects.get(id=pk)
            if user.role.lower() == 'admin':
                event.delete()
                return Response({'message': 'Event deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'You don\'t have permission to delete'}, status=status.HTTP_403_FORBIDDEN)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)


# Create your views here.
