from django.urls import path
from .views import OrderListCreateAPIView ,OrderByTokenAPIView,UserOrdersByTokenAPIView,AdminOrdersByTokenAPIView,OrdersScheduledAPIView,cancelOrderApiview,SingleOrderAPIView,AllactiveOrdersAPIView,AllactiveOrdersByUserAPIView

urlpatterns = [
    path('', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('order-by-token/<int:order_id>/', OrderByTokenAPIView.as_view(), name='order-detail'),
    path('user-orders/', UserOrdersByTokenAPIView.as_view(), name='user-orders'),
    path('all-orders/', AdminOrdersByTokenAPIView.as_view(), name='orders-by-token'),
    path('scheduled-orders/', OrdersScheduledAPIView.as_view(), name='scheduled-orders'),
    path('cancel-order/<int:order_id>/', cancelOrderApiview.as_view(), name='cancel-order'),
    path('single-order/<int:order_id>/', SingleOrderAPIView.as_view(), name='single-order'),
    path('active-orders/', AllactiveOrdersAPIView.as_view(), name='active-orders'),
    path('active-orders-by-user/', AllactiveOrdersByUserAPIView.as_view(), name='active-orders-by-user'),
]