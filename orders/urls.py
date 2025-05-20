from django.urls import path
from .views import OrderListCreateAPIView ,OrderByTokenAPIView,UserOrdersByTokenAPIView

urlpatterns = [
    path('', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('order-by-token/<int:order_id>/', OrderByTokenAPIView.as_view(), name='order-detail'),
    path('user-orders/', UserOrdersByTokenAPIView.as_view(), name='user-orders'),
]