from django.urls import path
from .views import BannerListCreateAPIView, BannerRetrieveUpdateDestroyAPIView


urlpatterns = [
    path('', BannerListCreateAPIView.as_view(), name='banner-list-create'),
    path('<int:pk>/', BannerRetrieveUpdateDestroyAPIView.as_view(), name='banner-detail'),
]