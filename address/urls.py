from address.views import AddressListCreateAPIview, AddressByTokenAPIView,UserAddressByTokenAPIView, DeleteAddressByTokenAPIView,AddressListByTokenAPIView
from django.urls import path


urlpatterns = [
    path('create/',AddressListCreateAPIview.as_view(),name='address-list-create'),
    path('<int:pk>/',AddressByTokenAPIView.as_view(),name='address-retrieve-update-destroy'),
    path('user-address/', UserAddressByTokenAPIView.as_view(), name='user-address-by-token'),
    path('delete-address/<int:pk>/', DeleteAddressByTokenAPIView.as_view(), name='delete-address-by-token'),
    path('', AddressListByTokenAPIView.as_view(), name='address-list-by-token'),

]
