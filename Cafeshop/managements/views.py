from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from product.forms import FruitForm,OptionForm,DrinkForm,PromotionForm
from product.models import Fruit,Drink_info,Option
# Create your views here.
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


@login_required
def add_fruit(request):
    if request.method == 'POST':
        form = FruitForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_fruit')
    else:
        form = FruitForm()
    
    return render(request, 'managements/add_fruit.html', context={
        'form': form
    })

@login_required
def edit_fruit(request, pk):
    f = Fruit.objects.get(id=pk)
    form = FruitForm(instance=f)
    if request.method == "POST":
        form = FruitForm(request.POST,request.FILES,instance=f)
        if form.is_valid():
            form.save()
            return redirect('list_fruit')
    context={
        'form': form,
        'f':f,
    }
    return render(request, 'managements/add_fruit.html', context) 

@login_required
def delete_fruit(request, pk):
    f = Fruit.objects.get(id=pk)
    f.delete()
    return  redirect('list_fruit')

@login_required
def add_option(request):
    if request.method == 'POST':
        form = OptionForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_option')
    else:
        form = OptionForm()
    
    return render(request, 'managements/add_option.html', context={
        'form': form
    })

@login_required
def edit_option(request, pk):
    o = Option.objects.get(id=pk)
    form = OptionForm(instance=o)
    if request.method == "POST":
        form = OptionForm(request.POST,request.FILES,instance=o)
        if form.is_valid():
            form.save()
            return redirect('list_option')
    context={
        'form': form,
        'o':o,
    }
    return render(request, 'managements/add_option.html', context)

@login_required
def delete_option(request, pk):
    o = Option.objects.get(id=pk)
    o.delete()
    return redirect('list_option')

@login_required
def add_drink(request):
    if request.method == 'POST':
        form = DrinkForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_drink')
    else:
        form = DrinkForm()
    
    return render(request, 'managements/add_drink.html', context={
        'form': form
    })

@login_required
def edit_drink(request, pk):
    d = Drink_info.objects.get(id=pk)
    form = DrinkForm(instance=d)
    if request.method == "POST":
        form = DrinkForm(request.POST,request.FILES,instance=d)
        if form.is_valid():
            form.save()
            return redirect('list_drink')
    context={
        'form': form,
        'd':d,
    }
    return render(request, 'managements/add_drink.html', context) 

@login_required
def delete_drink(request, pk):
    d = Drink_info.objects.get(id=pk)
    d.delete()
    return redirect('list_drink')

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
