# from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms

class MyUserFormUser(UserCreationForm):
    class Meta:
        model=Users
        fields=('first_name','last_name','username','phone','email','password1','password2')
        help_texts = {
            'password1': ('Must contain two special characters'),
        }
        
        def _init_(self, args ,*kwargs):
            super(AddressForm, self)._init_(args ,*kwargs)
            self.fields['username'].widget.attrs.update(
                {'name':'username'})
            self.fields['email'].widget.attrs.update(
                {'name':'email'})
            self.fields['phone'].widget.attrs.update(
                {'name':'phone','type':'number'})
        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=Users
        fields=('first_name','last_name','username','phone','email','propic')
        
        
DEMO_CHOICES =(
    ("Home", "Home"),
    ("Work", "Work"),
)
class MyAddressForm(forms.ModelForm):
    class Meta:
        model=Address
        fields=('fname','lname','address','city','pincode','state','phone','type')
        
        