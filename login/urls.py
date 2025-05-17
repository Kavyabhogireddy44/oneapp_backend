from django.urls import path
from .views import CreateTokenAPIView, VerifyTokenAPIView

urlpatterns = [
    path('create-token/', CreateTokenAPIView.as_view(), name='create-token'),
    path('verify-token/', VerifyTokenAPIView.as_view(), name='verify-token'),
]