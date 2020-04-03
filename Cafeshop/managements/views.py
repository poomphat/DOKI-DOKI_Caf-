from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from product.forms import FruitForm,OptionForm
from product.models import Fruit
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