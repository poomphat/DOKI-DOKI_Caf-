from django.shortcuts import render,redirect
from product.models import Order, Order_list, Drink_info
from django.db.models.functions import TruncMonth,TruncYear,Trunc,ExtractWeek
from django.db.models import Count, Sum
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.auth.decorators import login_required, permission_required
import json, datetime
# Create your views here.

@permission_required('auth.view_report')
@login_required
def report(request, report_type):
    report_type = report_type
    orders = Order.objects.filter(finish_flag=True)
    if report_type == 'month':
        orders = orders.annotate(time=Trunc('date', 'month')).values('time').annotate(count=Count('id'), total_income=Sum('total_price'))
    elif report_type == 'day':
        orders = orders.annotate(time=Trunc('date', 'day')).values('time').annotate(count=Count('id'), total_income=Sum('total_price'))
    elif report_type == 'year':
        orders = orders.annotate(time=Trunc('date', 'year')).values('time').annotate(count=Count('id'), total_income=Sum('total_price'))
    elif report_type == 'week':
        orders = orders.annotate(time=Trunc('date', 'week')).values('time').annotate(count=Count('id'), total_income=Sum('total_price'), week=ExtractWeek('time'))
    return render(request, 'report/report.html', context={'orders':orders,'type':report_type,})

@login_required
@csrf_exempt
def api_getOrderAtTime(request, report_type):
    if request.method == "POST":
        data = json.loads(request.body)['get']
        order_lists = Order_list.objects.all()
        if report_type == 'day':
            time = datetime.datetime.strptime(data['time'], '%B %d, %Y')
            order_lists = Order_list.objects.filter(order_id__date__date=time, order_id__finish_flag=True).values('order_id', 'd_id').annotate(count=Sum('amount'))
        elif report_type == 'month':
            order_lists = Order_list.objects.filter(order_id__date__month=data['time'], order_id__finish_flag=True).values('order_id', 'd_id').annotate(count=Sum('amount'))
        elif report_type == 'year':
            order_lists = Order_list.objects.filter(order_id__date__year=data['time'], order_id__finish_flag=True).values('order_id', 'd_id').annotate(count=Sum('amount'))
        if report_type == 'week':
            order_lists = Order_list.objects.filter(order_id__date__week=data['time'], order_id__finish_flag=True).values('order_id', 'd_id').annotate(count=Sum('amount'))
        the_list = []
        for order_list in order_lists:
            item = {
                'order_id':order_list['order_id'],
                'drink':Drink_info.objects.get(pk=order_list['d_id']).d_name,
                'amount':order_list['count'],
                'type':Drink_info.objects.get(pk=order_list['d_id']).drink_type
            }
            the_list.append(item)
        data = json.dumps(the_list)
    return HttpResponse(data, status=200)