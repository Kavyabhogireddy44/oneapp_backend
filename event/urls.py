from django.urls import path
from .views import EventListCreateAPIView, EventRetrieveUpdateAPIView,EventsByTokenAPIView,EventsListByTokenAPIView

urlpatterns = [
    path('', EventListCreateAPIView.as_view(), name='event-list-create'),
    path('<int:pk>/', EventRetrieveUpdateAPIView.as_view(), name='event-detail'),
    path('events-by-token/', EventsByTokenAPIView.as_view(), name='events-by-token'),
    path('events-by-token/',EventsListByTokenAPIView.as_view(), name='events-list-by-token'),
]