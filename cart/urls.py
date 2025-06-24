from django.urls import path
from .views import CreateCartView, ViewCartAPIView, UpdateCartItemAPIView, DeleteCartItemAPIView

urlpatterns = [
    path('create/', CreateCartView.as_view(), name='create_cart'),
    path('view/', ViewCartAPIView.as_view(), name='view_cart'),
    path('update/', UpdateCartItemAPIView.as_view(), name='update_cart_item'),
    path('delete/', DeleteCartItemAPIView.as_view(), name='delete_cart_item'),
    
]