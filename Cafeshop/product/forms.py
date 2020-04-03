from django import forms
from product.models import Fruit , Option
# Create the form class.
class FruitForm(forms.ModelForm):
    fruit_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={ 'class' : 'form-control col-5' })
        )
    fruit_desc = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={ 'class' : 'form-control col-12' })
        )
    class Meta:
        model = Fruit
        fields = ('fruit_name', 'fruit_desc')


class OptionForm(forms.ModelForm):
    option_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={ 'class' : 'form-control col-5' })
        )
    description = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={ 'class' : 'form-control col-12' })
        )
    price = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'type':'number', 'class' : 'form-control col-12'}))
    class Meta:
        model = Option
        fields = ('option_name', 'description','price')