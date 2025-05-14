from django.urls import path
from .views import UserListCreateAPIView, UserRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),
]