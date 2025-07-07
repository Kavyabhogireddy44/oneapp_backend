from django.urls import path
from .views import MetadataListCreateAPIView, MetadataRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', MetadataListCreateAPIView.as_view(), name='metadata-list-create'),
    path('<int:pk>/', MetadataRetrieveUpdateDestroyAPIView.as_view(), name='metadata-detail'),
    # path('otp-auth/', otp_auth, name='otp-auth'),
]