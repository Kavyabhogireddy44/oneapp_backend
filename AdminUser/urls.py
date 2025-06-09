from AdminUser.models import AdminUser
from django.urls import path
from AdminUser.views import  AdminCreateAPIView

urlpatterns = [
    path('admin-create/', AdminCreateAPIView.as_view(), name='admin-create'),
]