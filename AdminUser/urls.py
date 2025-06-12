from AdminUser.models import AdminUser
from django.urls import path
from AdminUser.views import  AdminCreateAPIView, AdminListAPIView,AdminDetailAPIView,AdminDeleteAPIView

urlpatterns = [
    path('admin-create/', AdminCreateAPIView.as_view(), name='admin-create'),
    path('admin-list/', AdminListAPIView.as_view(), name='admin-list'),
    path('admin-detail/<int:pk>/', AdminDetailAPIView.as_view(), name='admin-detail'),
    path('admin-delete/<int:pk>/', AdminDeleteAPIView.as_view(), name='admin-delete'),
]