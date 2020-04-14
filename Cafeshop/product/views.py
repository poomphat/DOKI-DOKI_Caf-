from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from product.models import Fruit, Drink_info,Customer,Option
from product.forms import UserForm,CustomerForm
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
    drink_infos = Drink_info.objects.all()
    options = Option.objects.all()
    fruits = Fruit.objects.all()
    context = {
        'drink_infos' : drink_infos,
        'options' : options,
        'fruits' : fruits,
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