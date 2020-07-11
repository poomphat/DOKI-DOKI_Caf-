from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,permission_required
from product.forms import FruitForm,OptionForm,DrinkForm,PromotionForm,Promotion
from product.models import Fruit, Drink_info,Customer,Option,Promotion,Order,Order_list,Special,Juice,Fruit,Juice_fruit,Coffee_and_other,Option,Juice_option,Coffee_and_other_option,Promotion,User
# Create your views here.

@permission_required('product.add_promotion')
@login_required
def add_promotion(request):
    if request.method == 'POST':
        form = PromotionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PromotionForm()
    
    return render(request, 'managements/add_promo.html', context={
        'form': form
    })


@permission_required('product.delete_promotion')
@login_required
def delete_promotion(request, pk):
    p = Promotion.objects.get(id=pk)
    p.promo_status == False
    p.save()
    return  redirect('index')

@permission_required('product.change_promotion')
@login_required
def edit_promotion(request, pk):
    p = Promotion.objects.get(id=pk)
    form = PromotionForm(instance=p)
    if request.method == "POST":
        form = PromotionForm(request.POST,instance=p)
        if form.is_valid():
            form.save()
            return redirect('index')
    context={
        'form': form,
        'p':p,
    }
    return render(request, 'managements/add_promo.html', context) 

@permission_required('product.add_fruit')
@login_required
def add_fruit(request):
    if request.method == 'POST':
        form = FruitForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_fruit', 'True')
    else:
        form = FruitForm()
    
    return render(request, 'managements/add_fruit.html', context={
        'form': form
    })

@permission_required('product.change_fruit')
@login_required
def edit_fruit(request, pk):
    f = Fruit.objects.get(id=pk)
    form = FruitForm(instance=f)
    if request.method == "POST":
        form = FruitForm(request.POST,request.FILES,instance=f)
        if form.is_valid():
            form.save()
            return redirect('list_fruit', 'True')
    context={
        'form': form,
        'f':f,
    }
    return render(request, 'managements/add_fruit.html', context) 

@permission_required('product.delete_fruit')
@login_required
def delete_fruit(request, pk):
    f = Fruit.objects.get(id=pk)
    if f.useable_status:
        f.useable_status = False
        f.save()
        return redirect('list_fruit', status='True')
    else:
        f.useable_status = True
        f.save()
        return redirect('list_fruit', status='False')

@permission_required('product.add_option')
@login_required
def add_option(request):
    if request.method == 'POST':
        form = OptionForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_option', 'True')
    else:
        form = OptionForm()
    
    return render(request, 'managements/add_option.html', context={
        'form': form
    })

@permission_required('product.change_option')
@login_required
def edit_option(request, pk):
    o = Option.objects.get(id=pk)
    form = OptionForm(instance=o)
    if request.method == "POST":
        form = OptionForm(request.POST,request.FILES,instance=o)
        if form.is_valid():
            form.save()
            return redirect('list_option', 'True')
    context={
        'form': form,
        'o':o,
    }
    return render(request, 'managements/add_option.html', context)


@login_required
@permission_required('product.delete_option')
def delete_option(request, pk):
    o = Option.objects.get(id=pk)
    if o.useable_status:
        o.useable_status = False
        o.save()
        return redirect('list_option', status='True')
    else:
        o.useable_status = True
        o.save()
        return redirect('list_option', status='False')

@permission_required('product.add_drink_info')
@login_required
def add_drink(request):
    if request.method == 'POST':
        form = DrinkForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_drink', 'True')
    else:
        form = DrinkForm()
    
    return render(request, 'managements/add_drink.html', context={
        'form': form
    })

@permission_required('product.change_drink_info')
@login_required
def edit_drink(request, pk):
    d = Drink_info.objects.get(id=pk)
    form = DrinkForm(instance=d)
    if request.method == "POST":
        form = DrinkForm(request.POST,request.FILES,instance=d)
        if form.is_valid():
            form.save()
            return redirect('list_drink', 'True')
    context={
        'form': form,
        'd':d,
    }
    return render(request, 'managements/add_drink.html', context) 

@permission_required('product.delete_drink_info')
@login_required
def delete_drink(request, pk):
    if pk != 1:
        d = Drink_info.objects.get(id=pk)
        if d.useable_status:
            d.useable_status = False
            d.save()
            return redirect('list_drink', status='True')
        else:
            d.useable_status = True
            d.save()
            return redirect('list_drink', status='False')
    else:
        return redirect('list_drink', status='True')

@permission_required('product.view_drink_info')
@login_required
def list_drink(request, status):
    drink_info = Drink_info.objects.all()
    if status == 'True':
        drink_info = drink_info.filter(useable_status=True)
    else:
        drink_info = drink_info.filter(useable_status=False)
    search = request.GET.get('search','')
    drink_info = drink_info.filter(d_name__icontains=search)
    context = {
        'drink_info' : drink_info,
        'status' : status
    }
    return render(request, 'managements/list_drink.html', context)
@permission_required('product.view_fruit')
@login_required
def list_fruit(request, status):
    fruit = Fruit.objects.all()
    if status == 'True':
        fruit = fruit.filter(useable_status=True)
    else:
        fruit = fruit.filter(useable_status=False)
    search = request.GET.get('search','')
    fruit = fruit.filter(fruit_name__icontains=search)
    context = {
        'fruit' : fruit,
        'status' : status
    }
    return render(request, 'managements/list_fruit.html', context)

@permission_required('product.view_option')
@login_required
def list_option(request, status):
    option = Option.objects.all()
    if status == 'True':
        option = option.filter(useable_status=True)
    else:
        option = option.filter(useable_status=False)
    search = request.GET.get('search','')
    option = option.filter(option_name__icontains=search)
    context = {
        'option' : option,
        'status' : status
    }
    return render(request, 'managements/list_option.html', context)

@login_required
def user_info(request):

    orders = Order.objects.filter(c_id = Customer.objects.get(user__id=request.user.id), finish_flag=True).order_by('-date')
    yourorders = []
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
            'order_type':order.order_type,
        }
        yourorders.append(order_list)
    context = {
        'yourOrders':yourorders
    }
    return render(request, 'managements/profile_report.html', context=context)
