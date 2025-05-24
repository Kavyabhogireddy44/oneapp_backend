from suggestions.views import SuggestionListCreateAPIView,SuggestionByTokenAPIView,UserSuggestionByTokenAPIView,DeleteSuggestionByTokenAPIView
from django.urls import path

urlpatterns = [
    path('', SuggestionListCreateAPIView.as_view(), name='suggestion-list-create'),
    path('<int:pk>/', SuggestionByTokenAPIView.as_view(), name='suggestion-detail'),
    path('user-suggestion/', UserSuggestionByTokenAPIView.as_view(), name='user-suggestion-by-token'),
    path('delete-suggestion/<int:pk>/', DeleteSuggestionByTokenAPIView.as_view(), name='delete-suggestion-by-token'),
]