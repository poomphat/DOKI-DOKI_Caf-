from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from product.forms import FruitForm,OptionForm,DrinkForm
from product.models import Fruit,Drink_info,Option
# Create your views here.



@login_required
def add_fruit(request):
    if request.method == 'POST':
        form = FruitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = FruitForm()
    
    return render(request, 'managements/add_fruit.html', context={
        'form': form
    })



@login_required
def add_option(request):
    if request.method == 'POST':
        form = OptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = OptionForm()
    
    return render(request, 'managements/add_option.html', context={
        'form': form
    })

@login_required
def add_drink(request):
    if request.method == 'POST':
        form = DrinkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = DrinkForm()
    
    return render(request, 'managements/add_drink.html', context={
        'form': form
    })
@login_required
def list_drink(request):
    drink_info = Drink_info.objects.all()
    search = request.GET.get('search','')
    drink_info = Drink_info.objects.filter(d_name__icontains=search)
    context = {
        'drink_info' : drink_info
    }
    return render(request, 'managements/list_drink.html', context)

@login_required
def list_fruit(request):
    fruit = Fruit.objects.all()
    search = request.GET.get('search','')
    fruit = Fruit.objects.filter(fruit_name__icontains=search)
    context = {
        'fruit' : fruit
    }
    return render(request, 'managements/list_fruit.html', context)
    
@login_required
def list_option(request):
    option = Option.objects.all()
    search = request.GET.get('search','')
    option = Option.objects.filter(option_name__icontains=search)
    context = {
        'option' : option
    }
    return render(request, 'managements/list_option.html', context)