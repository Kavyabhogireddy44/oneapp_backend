from django.urls import path
from .views import TicketUserCreateAPIView,TicketUserListAPIView ,TicketAdminListAPIView,  TicketAdminDeleteAPIView, TicketAdminUpdateAPIView, TicketAdmincreateadminAPIView

urlpatterns = [
    path('user-ticket-create/', TicketUserCreateAPIView.as_view(), name='ticket-user-create'),
    path('user-ticket-list/', TicketUserListAPIView.as_view(), name='ticket-user-list'),
    path('admin-ticket-delete/<int:ticket_id>/', TicketAdminDeleteAPIView.as_view(), name='ticket-admin-delete'),
    path('admin-ticket-update/<int:ticket_id>/', TicketAdminUpdateAPIView.as_view(), name='ticket-admin-update'),
    path('admin-ticket-create/', TicketAdmincreateadminAPIView.as_view(), name='ticket-admin-create'),
    path('admin-ticket-list/', TicketAdminListAPIView.as_view(), name='ticket-admin-list')
]