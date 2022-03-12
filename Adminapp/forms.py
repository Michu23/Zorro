from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *
from Userapp.models import *
from django import forms


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('catogery','ptype','btype','name','stocks','description','price','offerpercent','image1','image2','image3','image4')
        labels = {
            'catogery': 'Catogery :',
            'ptype': 'Price Type :',
            'btype': 'Brand :',
            'name': 'Name : ',
            'stocks': 'Stocks : ',
            'description': 'Description : ',
            'price': 'Price : ',
            'offerpercent': 'Offer Percent (%) :',
            'image1': 'Image 1 : ',
            'image2': 'Image 2 : ',
            'image3': 'Image 3 : ',
            'image4': 'Image 4 : ',
        }
        help_texts = {
            'offerpercent': ('Enter the offerpercent you want to give if the offer is applied'),
        }
   
class MyCatForm(forms.ModelForm):
    class Meta:
        model=Catogery
        fields='__all__'
        
class MyBrandForm(forms.ModelForm):
    class Meta:
        model=Brand
        fields='__all__'
        
        
class MyPriceForm(forms.ModelForm):
    class Meta:
        model=PriceType
        fields='__all__'

class MyCouponForm(forms.ModelForm):
    class Meta:
        model=CouponDetail
        fields='__all__'
        
        
