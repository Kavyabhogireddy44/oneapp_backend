from django.urls import path
from .views import AreaPolygonListCreateAPIView, AreaPolygonDetailAPIView

urlpatterns = [
    path('', AreaPolygonListCreateAPIView.as_view(), name='area-polygon-list-create'),
    path('<int:pk>/', AreaPolygonDetailAPIView.as_view(), name='area-polygon-detail'),
]