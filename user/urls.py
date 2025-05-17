from django.urls import path
from .views import UserListCreateAPIView, UserRetrieveUpdateDestroyAPIView, CheckPhoneNumberAPIView

urlpatterns = [
    path('', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),
    path('check-phone/', CheckPhoneNumberAPIView.as_view(), name='check-phone'),
]