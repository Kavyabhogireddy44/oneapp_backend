from address.views import AddressListCreateAPIview, AddressByTokenAPIView
from django.urls import path


urlpatterns = [
    path('',AddressListCreateAPIview.as_view(),name='address-list-create'),
    path('<int:pk>/',AddressByTokenAPIView.as_view(),name='address-retrieve-update-destroy'),
]
