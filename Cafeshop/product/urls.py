"""Cefeshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from . import views
from django.urls import path,include

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.mylogin, name='login'),
    path('logout/', views.mylogout, name='logout'),
    path('register/', views.register, name='register'),
    path('api/', views.api, name='api'),
    path('api_drink/', views.api_drink, name='api_drink'),
    path('api_promotion/', views.api_promotion, name='api_promotion'),
    path('api_option/', views.api_option, name='api_option'),
    path('queue/', views.queue, name='queue'),
    path('order_success/<int:id>/', views.order_success, name='order_success'),
    path('account_manage/',views.account_manage, name='account_manage'),
]
