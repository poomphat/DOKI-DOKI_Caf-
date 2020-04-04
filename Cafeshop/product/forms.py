from django import forms
from product.models import Fruit , Option
# Create the form class.
class FruitForm(forms.ModelForm):
    fruit_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={ 'class' : 'form-control col-5',
                                        'placeholder' : 'ชื่อของผลไม้' }),
        
        label='Fruit name:'
        )
    fruit_desc = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={ 'class' : 'form-control col-12', 
                                        'placeholder' : 'คำอธิบายของผลไม้'}),
        
        label='Fruit description:'
        )
    class Meta:
        model = Fruit
        fields = ('fruit_name', 'fruit_desc')


class OptionForm(forms.ModelForm):
    option_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={ 'class' : 'form-control col-5', 'placeholder' : 'ชื่อของ topping' }),
        label='Topping name:'
        )
    description = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={ 'class' : 'form-control col-12' , 'placeholder' : 'คำอธิบายของ topping' }),
        label='Topping description:'
        )
    price = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'type':'number', 'class' : 'form-control col-12' ,'placeholder' : 'ราคาของ topping'}),
        label='Topping price:')
    class Meta:
        model = Option
        fields = ('option_name', 'description','price')