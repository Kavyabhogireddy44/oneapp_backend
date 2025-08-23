from django.urls import path
from .views import UserListCreateAPIView, CheckPhoneNumberAPIView, UserByTokenAPIView,DeleteUserByTokenAPIView, get_firebase_token, SendFCMToAllUsersAPIView

urlpatterns = [
    path('', UserListCreateAPIView.as_view(), name='user-list-create'),
    # path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
    # path('<int:pk>/delete/', UserDestroyAPIView.as_view(), name='user-delete'),   
    path('check-phone/', CheckPhoneNumberAPIView.as_view(), name='check-phone'),
    # path('user-by-token/', UserByTokenAPIView.as_view(), name='user-by-token'),
    path('user-by-token/', UserByTokenAPIView.as_view(), name='user-by-token'),
    path('delete-user/', DeleteUserByTokenAPIView.as_view(), name='delete-user-by-token'),
    path("get-token/", get_firebase_token, name="get_firebase_token"),
     path("send-to-all/", SendFCMToAllUsersAPIView.as_view(), name="send_fcm_to_all_users"),

]