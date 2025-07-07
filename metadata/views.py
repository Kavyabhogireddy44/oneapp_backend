from django.shortcuts import render
from rest_framework import generics 
from .models import MetaData
from .serializers import MetadataSerializer




# import random
# import datetime
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json

# import json
# import random
# import datetime
# import requests

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt


# otp_storage = {}


# # Use free test key from Textbelt
# TEXTBELT_API_KEY = 'textbelt'  # Paid key = 'your-paid-key'

# def send_sms(phone, otp):
#     # phone example: '919876543210' (country code + number, no + sign)
#     api_url = (
#         f"https://api.callmebot.com/whatsapp.php"
#         f"?phone={phone}"
#         f"&text=Your+OTP+is+{otp}"
#         f"&apikey=your_api_key"  # If you have one; it's optional for limited usage
#     )
#     response = requests.get(api_url)
#     print("CallMeBot response:", response.text)

# @csrf_exempt
# def otp_auth(request):
#     if request.method != 'POST':
#         return JsonResponse({'error': 'Only POST allowed'}, status=405)

#     try:
#         data = json.loads(request.body)
#         phone = data.get('phone')
#         otp = data.get('otp')  # Optional

#         if not phone:
#             return JsonResponse({'error': 'Phone number is required'}, status=400)

#         if not otp:
#             # Step 1: Send OTP
#             generated_otp = random.randint(100000, 999999)
#             otp_storage[phone] = {
#                 'otp': str(generated_otp),
#                 'expires_at': datetime.datetime.now() + datetime.timedelta(minutes=5)
#             }
#             print(f"Generated OTP for {phone}: {generated_otp}")
#             send_sms(phone, generated_otp)
#             return JsonResponse({'message': 'OTP sent successfully'})
#         else:
#             # Step 2: Verify OTP
#             otp_data = otp_storage.get(phone)
#             if not otp_data:
#                 return JsonResponse({'error': 'OTP expired or not sent'}, status=400)

#             if datetime.datetime.now() > otp_data['expires_at']:
#                 return JsonResponse({'error': 'OTP expired'}, status=400)

#             if otp_data['otp'] != str(otp):
#                 return JsonResponse({'error': 'Invalid OTP'}, status=400)

#             # Success - authentication done
#             # (You can generate a token here if needed)
#             return JsonResponse({'message': 'OTP verified successfully'})

#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)

class MetadataListCreateAPIView(generics.ListCreateAPIView):
    queryset = MetaData.objects.all()
    serializer_class = MetadataSerializer

class MetadataRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MetaData.objects.all()   
    serializer_class = MetadataSerializer

# Create your views here.
