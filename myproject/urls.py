"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('books.urls')),
    path('api/users/', include('user.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/favourites/', include('favourites.urls')),
    path('api/login/', include('login.urls')),
    path('api/address/', include('address.urls')),
    path('api/suggestions/', include('suggestions.urls')),
    path('api/banner/', include('banner.urls')),
    path('api/metadata/', include('metadata.urls')),
    path('api/event/', include('event.urls')),
    path('api/polygon/', include('polygon.urls')),
    path('api/adminuser/', include('AdminUser.urls')),
    path('api/adminuserlogin/', include('AdminUserLogin.urls')),
    path('api/grocery/', include('grocery.urls')),
    path('api/cart/', include('cart.urls')),  # Include cart URLs
    path('api/ticket/', include('ticket.urls')),  # Include ticket URLs

    
]