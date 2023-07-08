from attr import field
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Customer, Order, Product

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'       

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        
class LoginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email']
        

class AdditemForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

