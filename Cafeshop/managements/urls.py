from django.contrib import admin

from django.urls import path,include
from . import views
urlpatterns = [
    path('add_fruit/', views.add_fruit, name='add_fruit'),
    path('add_option/', views.add_option, name='add_option'),
    path('add_drink/', views.add_drink, name='add_drink'),
    path('list_drink/', views.list_drink, name='list_drink'),
    path('list_fruit/', views.list_fruit, name='list_fruit'),
    path('list_option/', views.list_option, name='list_option'),
    path('add_promotion/', views.add_promotion, name='add_promotion'),
    path('edit_fruit/<int:pk>/',views.edit_fruit, name='edit_fruit'),
    path('edit_option/<int:pk>/',views.edit_option, name='edit_option'),
    path('edit_drink/<int:pk>/',views.edit_drink, name='edit_drink'),
]