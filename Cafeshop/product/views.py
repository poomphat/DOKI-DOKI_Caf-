from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from product.models import Fruit, Drink_info,Customer,Option,Promotion,Order,Order_list,Special,Juice,Fruit,Juice_fruit,Coffee_and_other,Option,Juice_option,Coffee_and_other_option
from product.forms import UserForm,CustomerForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json
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
    promo = Promotion.objects.all()
    drink_infos = Drink_info.objects.exclude(id=8)
    options = Option.objects.all()
    fruits = Fruit.objects.all()
    context = {
        'drink_infos' : drink_infos,
        'options' : options,
        'fruits' : fruits,
        'Promotion' : promo,
    }
    print(fruits)
    return render(request, 'product/index.html', context=context)

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        Customer_form = CustomerForm(request.POST)
        if user_form.is_valid() and Customer_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            Customer = Customer_form.save(commit=False)
            Customer.user = user
            Customer.save()
            registered = True
        else:
            print(user_form.errors,CustomerForm.errors)
    else:
        user_form = UserForm()
        Customer_form = CustomerForm()

    context =  {'user_form':user_form,
                'Customer_form':Customer_form,
                'registered':registered}
    return render(request,'register.html', context)

@csrf_exempt
def api(request):
    data = json.loads(request.body)
    order_data = data['order']
    print(Customer.objects.get(pk=request.user.id).id)
    order = Order()
    order.c_id = Customer.objects.get(pk=request.user.id)
    order.total_price = order_data['total_price']
    order.promo_id = Promotion.objects.get(pk=1)
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

def delete_WARRING_PLZ_DONT_USE_THIS(request):
    a = Special.objects.all()
    for x in a:
        x.delete()
    return render(request,'product/queue.html', context={})

def queue(request):
    orders = Order.objects.all()
    queue = []
    for order in orders:
        order_lists = Order_list.objects.filter(order_id=order.id)
        item = {}
        for order_list in order_lists:
            item = {
                'id':order_list.d_id,
                'order_id':order_list.order_id,
                'unit_price':order_list.unit_price,
                'sweetness':'',
                'fruit':'',
                'topping':'',
                'amount':order_list.amount,
            }
            special = Special.objects.get(pk=order_list.special_id_id)
            if special.special_type == 'Coffee':
                coffee = Coffee.objects.get(pk=special.id)
                item['sweetness'] = coffee.sweetness
                co = coffee.option.all()
                topping_items = []
                for topping in co:
                    option = Option.objects.get(pk=topping.option_id)
                    topping_items.append({
                        'name':option.name,
                        'amount':topping.amount
                    })
                item['topping'] = topping_items
            elif special.special_type == 'Juice':
                juice = Juice.objects.get(pk=special.id)
                jo = juice.option.all()
                topping_items = []
                for topping in jo:
                    option = Option.objects.get(pk=topping.option_id)
                    topping_items.append({
                        'name':option.name,
                        'amount':topping.amount
                    })
                item['topping'] = topping_items
                jf = juice.fruit.all()
                fruit_items = []
                for juicefruit in jf:
                    fruit = Option.objects.get(pk=juicefruit.option_id)
                    fruit_items.append({
                        'name':fruit.name,
                        'amount':juicefruit.amount
                    })
                item['fruit'] = fruit_items
        order_list = {
            'id':order.id,
            'date':order.date,
            'promo_id':order.promo_id,
            'finish':order.finish_flag,
            'item':item,
            'total_price':order.total_price
        }
        queue.append(order_list)
    print(queue)
    context = {
        'queues':queue
    }
    return render(request,'product/queue.html', context=context)