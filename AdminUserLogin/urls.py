from django.urls import path
from AdminUserLogin.views import CreateTokenAPIView, VerifyTokenAPIView

urlpatterns = [
    path('admin-create-token/', CreateTokenAPIView.as_view(), name='create-token'), 
    path('admin-verify-token/', VerifyTokenAPIView.as_view(), name='verify-token'),

]