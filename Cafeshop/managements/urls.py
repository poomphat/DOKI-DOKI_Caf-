from django.contrib import admin

from django.urls import path,include
from . import views
urlpatterns = [
    path('add_fruit/', views.add_fruit, name='add_fruit'),
    path('add_option/', views.add_option, name='add_option'),
]
