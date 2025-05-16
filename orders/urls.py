from django.urls import path
from .views import OrderListCreateAPIView, OrderRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('<int:pk>/', OrderRetrieveUpdateDestroyAPIView.as_view(), name='order-detail'),
]