from django.shortcuts import render

from rest_framework import generics
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from login.utils import verify_jwt
from django.http import JsonResponse
from google.oauth2 import service_account
import google.auth.transport.requests
import os
from django.conf import settings
import json, requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser as User  # Adjust the import based on your project structure
from rest_framework.permissions import AllowAny
from google.auth.transport.requests import Request
import os
from google.oauth2 import service_account
import google.auth.transport.requests
from django.conf import settings

def get_firebase_token():
    """
    Returns a Firebase access token for FCM messaging.
    Works both locally and on Render.
    """
    SCOPES = ["https://www.googleapis.com/auth/firebase.messaging"]

    credentials = service_account.Credentials.from_service_account_file(
        settings.SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    credentials.refresh(google.auth.transport.requests.Request())
    return credentials.token






class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

# class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

# APP_DIR = os.path.dirname(os.path.abspath(__file__))

# # Path to JSON in same folder
# SERVICE_ACCOUNT_FILE = os.path.join(APP_DIR, "one_app.json")


# def get_firebase_token():

#     """Return Firebase access token string."""
#     SCOPES = [
#         "https://www.googleapis.com/auth/firebase.messaging"  # Required scope for sending FCM messages
#     ]
#     credentials = service_account.Credentials.from_service_account_file(
#         SERVICE_ACCOUNT_FILE, scopes=SCOPES
#     )
#     credentials.refresh(google.auth.transport.requests.Request())
#     return credentials.token


class SendFCMToAllUsersAPIView(APIView):
    permission_classes = [AllowAny]  # Optional: allow unauthenticated access for testing
    print("inside send fcm to all users api view")

    def post(self, request):
        try:
            payload = request.data  # DRF parses JSON automatically
            message = payload.get("message", {})
            notification = message.get("notification", {})
            data = message.get("data", {})
            android = message.get("android", {})
            print("payload", payload)
            print("notification", notification)
            print("data", data)
            print("android", android)


            # Collect all FCM tokens
            # tokens = list(CustomUser.objects.exclude(fcm_token__isnull=True).values_list("fcm_token", flat=True))
            tokens = ["cvX-ho_RSJ-g30sLv-WpSi:APA91bGky7m2dd6wf_pBbgIbOrUit_qeaSB32I-AZNw7ervyY6WYy9EHsTRZu4xNVmfC5wDRaLTP7wzE-W5FKO83JgZrNzQwn-BuF3Y4sCLmK-RvsJhstVI","cvX-ho_RSJ-g30sLv-WpSi:APA91bGky7m2dd6wf_pBbgIbOrUit_qeaSB32I-AZNw7ervyY6WYy9EHsTRZu4xNVmfC5wDRaLTP7wzE-W5FKO83JgZrNzQwn-BuF3Y4sCLmK-RvsJhstVI"]
            print("tokens", tokens)
            if not tokens:
                return Response({"error": "No FCM tokens found"}, status=status.HTTP_400_BAD_REQUEST)

            access_token = get_firebase_token()
            print("access_token", access_token)
            url = "https://fcm.googleapis.com/v1/projects/oneapp-74b5a/messages:send"
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json; UTF-8",
            }
            print("headers", headers)
            print("inside try block")

            results = []
            for token in tokens:
                print("token", token)
                fcm_payload = {
                    "message": {
                    "token": token,
                    "notification": notification,
                    "data": data,
                    "android": android
                    }
                }
                 
                print("fcm_payload", fcm_payload)
                response = requests.post(url, headers=headers, json=fcm_payload)
                try:
                    response_data = response.json()
                except:
                    response_data = response.text
                results.append({
                    "token": token,
                    "status": response.status_code,
                    "response": response_data
                })

            return Response({"results": results})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
# class UserByTokenAPIView(APIView):
#     def post(self, request):
#         token = request.data.get('token')
#         if not token:
#             return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
#         payload = verify_jwt(token)
#         print("payload", payload)
#         if not payload:
#             return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
#         user_id = payload.get('user_id')
#         print("user_id", user_id)
#         try:
#             user = CustomUser.objects.get(id=user_id)
#         except CustomUser.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#         serializer = UserSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
class CheckPhoneNumberAPIView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response(False, status=status.HTTP_200_OK)  # or return an error if preferred
        
        exists = CustomUser.objects.filter(phone=phone).exists()
        return Response(exists, status=status.HTTP_200_OK)
    
class UserByTokenAPIView(APIView):
    def get_user_from_token(self, token):
        if not token:
            return None, Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        payload = verify_jwt(token)
        if not payload:
            return None, Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = payload.get('user_id')
        try:
            user = CustomUser.objects.get(id=user_id)
            return user, None
        except CustomUser.DoesNotExist:
            return None, Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """Retrieve user by token."""
        token = request.data.get('token')
        user, error = self.get_user_from_token(token)
        if error:
            return error
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """Update user by token."""
        token = request.data.get('token')
        user, error = self.get_user_from_token(token)
        if error:
            return error

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteUserByTokenAPIView(APIView):
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
            user = CustomUser.objects.get(id=user_id)
            user=user.id
            print("user", user)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = CustomUser.objects.get(id=user_id)
        except user.DoesNotExist:
            return Response({'error': 'user not found for this user'}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({'message': 'user deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

