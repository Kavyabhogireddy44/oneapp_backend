
from django.urls import path
from .views import FavouriteListCreateAPIView, FavouriteRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', FavouriteListCreateAPIView.as_view(), name='favourite-list-create'),
    path('<int:pk>/', FavouriteRetrieveUpdateDestroyAPIView.as_view(), name='favourite-detail'),
]