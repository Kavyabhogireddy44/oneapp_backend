from suggestions.views import SuggestionListCreateAPIView,SuggestionByTokenAPIView,UserSuggestionByTokenAPIView,AdminDeleteSuggestionByTokenAPIView,AdminSuggestionByTokenAPIView
from django.urls import path

urlpatterns = [
    path('', SuggestionListCreateAPIView.as_view(), name='suggestion-list-create'),
    path('<int:pk>/', SuggestionByTokenAPIView.as_view(), name='suggestion-detail'),
    path('user-suggestion/', UserSuggestionByTokenAPIView.as_view(), name='user-suggestion-by-token'),
    path('delete-suggestion/<int:pk>/', AdminDeleteSuggestionByTokenAPIView.as_view(), name='delete-suggestion-by-token'),
    path('admin-suggestion/', AdminSuggestionByTokenAPIView.as_view(), name='admin-suggestion-by-token'),
]