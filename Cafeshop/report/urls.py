from django.contrib import admin
from . import views
from django.urls import path,include

urlpatterns = [
    path('<str:report_type>/', views.report, name='report'),
    path('<str:report_type>/api-report-order/', views.api_getOrderAtTime, name='get_order_at_time'),
]