from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('catogery','ptype','btype','name','stocks','description','price','image1','image2','image3','image4')
        labels = {
            'catogery': 'Catogery :',
            'ptype': 'Price Type :',
            'btype': 'Brand :',
            'name': 'Name : ',
            'stocks': 'Stocks : ',
            'description': 'Description : ',
            'price': 'Price : ',
            'image1': 'Image 1 : ',
            'image2': 'Image 2 : ',
            'image3': 'Image 3 : ',
            'image4': 'Image 4 : ',
        }
        
        
        
