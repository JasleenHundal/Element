"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from user_management.views import home_view, user_list_view, register,login_view, UserViewSet
from client_details.views import client_list_view, clients_view, ClientViewSet, client_list, client_detail, actions
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'clients', ClientViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path('user-management/', include('user_management.urls')),
    path('client-details/', include('client_details.urls')),
    path('', home_view, name='home'),  
    path('users/', user_list_view, name='user-list'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('api/', include(router.urls)),
    path('clients/', clients_view, name='client-list'),
    path('api/clients/', client_list, name='client_list'),
    path('api/clients/<int:client_id>/', client_detail, name='client_detail'),
    path('actions/', actions, name='actions'),



]
