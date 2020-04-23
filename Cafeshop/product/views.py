from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import update_session_auth_hash
from product.models import Fruit, Drink_info,Customer,Option,Promotion,Order,Order_list,Special,Juice,Fruit,Juice_fruit,Coffee_and_other,Option,Juice_option,Coffee_and_other_option,Promotion
from product.forms import UserForm,CustomerForm,UserForm2
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth.models import Group
from django.utils import timezone
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
import json, datetime
# Create your views here.

def mylogin(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('index')
        else:
            context['username'] = username
            context['password'] = password
            context['error'] = 'Wrong username or password!'

    return render(request, 'login.html',context)



def mylogout(request):
    logout(request)
    return redirect('login')
    
    
@login_required
def index(request):
    promotions = Promotion.objects.all()
    for promotion in promotions:
        if promotion.e_date < datetime.date.today():
            promotion.promo_status = False
            promotion.save()
    promotions = promotions.filter(promo_status = True)
    drink_infos = Drink_info.objects.exclude(id=1).filter(useable_status=True)
    print(drink_infos)
    options = Option.objects.filter(useable_status=True)
    fruits = Fruit.objects.filter(useable_status=True)
    context = {
        'drink_infos' : drink_infos,
        'options' : options,
        'fruits' : fruits,
        'Promotion' : promotions,
    }
    return render(request, 'product/index.html', context=context)

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        Customer_form = CustomerForm(request.POST,request.FILES)
        if user_form.is_valid() and Customer_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            Customer = Customer_form.save(commit=False)
            Customer.user = user
            Customer.save()
            group = Group.objects.get(name='Customer')
            user.groups.add(group)
            registered = True
            #return redirect('login')
        else:
            print(user_form.errors,CustomerForm.errors)
    else:
        Customer_form = CustomerForm()
        user_form = UserForm()
        

    context =  {'user_form':user_form,
                'Customer_form':Customer_form,
                'registered':registered}
    return render(request,'register.html', context)

@login_required
def account_manage(request):
    if request.method == 'POST':
        form = UserForm2(request.POST, instance=request.user)
        Customer_form = CustomerForm(request.POST, request.FILES, instance=request.user.customer)
        
        if form.is_valid() and Customer_form.is_valid():
            user = form.save()
            user.save()
            Customer = Customer_form.save(commit=False)
            Customer.user = user
            Customer.save()
            group = Group.objects.get(name='Customer')
            user.groups.add(group)

            return redirect('user_info')
        else:
            print(form.errors,CustomerForm.errors) 
    else:
        form = UserForm2(instance=request.user)
        Customer_form = CustomerForm(instance=request.user.customer)
                     
    context={
                'form':form,
                'Customer_form':Customer_form
                }
    return render(request,'account_manage.html', context)

@login_required
def password_reset(request):
    repass = False
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            repass = True
    else:
        form = PasswordChangeForm(user=request.user)
    context = {
        'form':form,
        'repass':repass
    }
    return render(request, 'password_reset.html', context)


@csrf_exempt
def api(request):
    data = json.loads(request.body)
    order_data = data['order']
    print(order_data, 'WHEN ORDER COME')
    order = Order()
    if request.user.id != 1 :
        order.c_id = Customer.objects.get(user__id=request.user.id)#instance
        order.order_type = 'Online_buy'
    else :
        order.c_id = None
        order.order_type = 'Local_buy'
    order.total_price = order_data['total_price']
    if order_data['promotion'] == 0:
        order.promo_id = None
    else:
        order.promo_id = Promotion.objects.get(pk=order_data['promotion'])
    order.save()
    for item in order_data['cart']:
        order_list = Order_list()
        order_list.amount = item['amount']
        order_list.unit_price = item['price_incTopping']
        order_list.d_id = Drink_info.objects.get(pk=item['id'])
        special = Special(special_type=item['kind'].capitalize()) 
        special.save()
        order_list.special_id = special
        order_list.order_id = order
        order_list.save()
        if item['kind'] == 'juice':
            juice = Juice()
            juice.special_id = special
            juice.save()
            for fruit in item['fruit']:
                jf = Juice_fruit()
                jf.juice = juice
                jf.fruit = Fruit.objects.get(pk=fruit['id'])
                jf.amount = 1
                jf.save()
            for option in item['topping_list']:
                jo = Juice_option()
                jo.juice = juice 
                jo.option = Option.objects.get(pk=option['id'])
                jo.amount = option['amount']
                jo.save()
        elif item['kind'] == 'coffee':
            coffee = Coffee_and_other()
            coffee.specials = special
            coffee.sweetness = item['sweetness']
            coffee.save()
            for option in item['topping_list']:
                co = Coffee_and_other_option()
                co.option = Option.objects.get(pk=option['id'])
                co.Coffee_and_other = coffee
                co.amount = option['amount']
                co.save()
        #order.save()
    return JsonResponse(order_data, status=200)

@login_required
def queue(request):
    print(timezone.now())
    orders = Order.objects.filter(finish_flag=False)
    queue = []
    sweetness_name = {
    'normalsweet': 'หวานปกติ',
    'lesssweet': 'หวานน้อย',
    'moresweet': 'หวานมาก',
    }
    for order in orders:
        order_lists = Order_list.objects.filter(order_id=order.id)
        item_list = []
        item = {}
        for order_list in order_lists:
            item = {
                'id':order_list.d_id_id,
                'order_id':order_list.order_id_id,
                'unit_price':order_list.unit_price,
                'sweetness':None,
                'fruits':None,
                'toppings':None,
                'amount':order_list.amount,
                'picture':Drink_info.objects.get(pk=order_list.d_id_id).picture,
                'how_to_make':Drink_info.objects.get(pk=order_list.d_id_id).how_to_make,
                'name':Drink_info.objects.get(pk=order_list.d_id_id).d_name
            }
            special = Special.objects.get(pk=order_list.special_id_id)
            if special.special_type == 'Coffee':
                coffee = Coffee_and_other.objects.get(pk=special.id)
                item['sweetness'] = sweetness_name[coffee.sweetness]
                toppings = coffee.options.all()
                topping_items = []
                for topping in toppings:
                    co = Coffee_and_other_option.objects.get(Coffee_and_other=coffee, option=topping)
                    topping_items.append({
                        'name':topping.option_name,
                        'amount':co.amount
                    })
                item['toppings'] = topping_items
            elif special.special_type == 'Juice':
                juice = Juice.objects.get(pk=special.id)
                toppings = juice.options.all()
                topping_items = []
                for topping in toppings:
                    jo = Juice_option.objects.get(juice=juice, option=topping)
                    topping_items.append({
                        'name':topping.option_name,
                        'amount':jo.amount
                    })
                item['toppings'] = topping_items
                fruits = juice.fruits.all()
                fruit_items = []
                for fruit in fruits:
                    jf = Juice_fruit.objects.get(juice=juice, fruit=fruit)
                    fruit_items.append({
                        'name':fruit.fruit_name,
                        'amount':jf.amount
                    })
                item['fruits'] = fruit_items
            item_list.append(item)
        order_list = {
            'id':order.id,
            'date':order.date,
            'promo_id':order.promo_id,
            'finish':order.finish_flag,
            'items':item_list,
            'time':order.date.strftime('%H:%M'),
            'total_price':order.total_price,
            'your':False,
            'order_type':order.order_type,
            'customer_name':None
        }
        if (request.user.id != 1):
            if(order.c_id != None):
                order_list['customer_name'] = order.c_id.user.first_name
                if Customer.objects.get(user__id=request.user.id).id == order.c_id.id:
                    order_list['your'] = True
        queue.append(order_list)
    context = {
        'queues':queue
    }
    return render(request,'product/queue.html', context=context)
    
@login_required    
def order_success(request, id):
    order = Order.objects.get(pk=id)
    order.finish_flag = True
    order.save()
    return redirect('queue')

@csrf_exempt
def api_drink(request):
    data = {}   
    drink_infos = Drink_info.objects.exclude(id=1).filter(useable_status=True)
    if request.method == 'GET':
        data = serializers.serialize("json", drink_infos)
    return HttpResponse(data, status=200)

@csrf_exempt
def api_promotion(request):
    data = json.loads(request.body)
    res = {
        'discount':0
    }
    print(data)
    if int(data['id']) != 0:
        promotion = Promotion.objects.get(pk=data['id'])
        res = {
            'discount':promotion.discount
        }
    return JsonResponse(res, status=200)

@csrf_exempt
def api_option(request):
    data = {}   
    options = Option.objects.filter(useable_status=True)
    if request.method == 'GET':
        data = serializers.serialize("json", options)
    return HttpResponse(data, status=200)