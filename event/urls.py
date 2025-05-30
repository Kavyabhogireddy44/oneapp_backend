from django.urls import path
from .views import EventListCreateAPIView, EventRetrieveUpdateAPIView,EventsByTokenAPIView,EventsListByTokenAPIView,DeleteEventsByTokenAPIView

urlpatterns = [
    path('', EventListCreateAPIView.as_view(), name='event-list-create'),
    path('<int:pk>/', EventRetrieveUpdateAPIView.as_view(), name='event-detail'),
    path('event-by-token/', EventsByTokenAPIView.as_view(), name='events-by-token'),
    path('events-by-token/',EventsListByTokenAPIView.as_view(), name='events-list-by-token'),
    path('delete-events-by-token/',DeleteEventsByTokenAPIView.as_view(), name='delete-events-by-token'),
]