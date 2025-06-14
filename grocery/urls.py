from .models import GroceryItem
from django.urls import path
from .views import GroceryCreateAPIView, GroceryListAPIView, GroceryDetailAPIView,  GroceryDeleteAPIView

urlpatterns = [
    path('grocery-create/', GroceryCreateAPIView.as_view(), name='grocery-create'),
    path('grocery-list/', GroceryListAPIView.as_view(), name='grocery-list'),
    path('grocery-detail/<int:pk>/', GroceryDetailAPIView.as_view(), name='grocery-detail'),
    path('grocery-delete/<int:pk>/', GroceryDeleteAPIView.as_view(), name='grocery-delete'),
]
