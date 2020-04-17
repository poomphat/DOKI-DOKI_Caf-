from django.shortcuts import render,redirect
from product.models import Order, Order_list
from django.db.models.functions import TruncMonth,TruncYear,Trunc,ExtractWeek
from django.db.models import Count, Sum
from django.http import HttpResponse
# Create your views here.

def report(request, report_type):
    report_type = report_type
    orders = Order.objects.all()
    if report_type == 'month':
        orders = orders.annotate(time=Trunc('date', 'month')).values('time').annotate(count=Count('id'), total_income=Sum('total_price'))
    elif report_type == 'day':
        orders = orders.annotate(time=Trunc('date', 'day')).values('time').annotate(count=Count('id'), total_income=Sum('total_price'))
    elif report_type == 'year':
        orders = orders.annotate(time=Trunc('date', 'year')).values('time').annotate(count=Count('id'), total_income=Sum('total_price'))
    elif report_type == 'week':
        orders = orders.annotate(time=Trunc('date', 'week')).values('time').annotate(count=Count('id'), total_income=Sum('total_price'), week=ExtractWeek('time'))
    return render(request, 'report/report.html', context={'orders':orders,'type':report_type,})