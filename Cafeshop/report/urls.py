from django.contrib import admin
from . import views
from django.urls import path,include

urlpatterns = [
    path('<str:report_type>/', views.report, name='report'),
]