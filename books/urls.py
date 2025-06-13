from django.urls import path
from .views import ServiceListCreateAPIView, ServiceRetrieveUpdateDestroyAPIView,ActiveServiceListAPIView, ServicesCountAPIView

urlpatterns = [
    path('services/', ServiceListCreateAPIView.as_view(), name='service-list-create'),
    path('services/<int:pk>/', ServiceRetrieveUpdateDestroyAPIView.as_view(), name='service-detail'),
    path('services/active/', ActiveServiceListAPIView.as_view(), name='active-service-list'),
    path('services/count/', ServicesCountAPIView.as_view(), name='services-count'),
]
