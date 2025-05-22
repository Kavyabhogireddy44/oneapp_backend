from suggestions.views import SuggestionListCreateAPIView,SuggestionByTokenAPIView
from django.urls import path

urlpatterns = [
    path('', SuggestionListCreateAPIView.as_view(), name='suggestion-list-create'),
    path('<int:pk>/', SuggestionByTokenAPIView.as_view(), name='suggestion-detail'),
]