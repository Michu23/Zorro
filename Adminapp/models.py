from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Catogery(models.Model):
    name=models.CharField(max_length=100,null=True)
    
    def __str__(self):
        return self.name

    
class PriceType(models.Model):
    genre = models.CharField(max_length = 20,null=True,blank=True)

    def __str__(self):
        return self.genre
    
class Brand(models.Model):
    bname = models.CharField(max_length = 20,null=True,blank=True)
    
    def __str__(self):
        return self.bname
    

    
class Product(models.Model):
    name=models.CharField(max_length=100,null=True)
    description=models.TextField(max_length=500,null=True)
    price=models.FloatField(null=True)
    image1=models.ImageField(upload_to='images',blank=True)
    image2=models.ImageField(upload_to='images',blank=True)
    image3=models.ImageField(upload_to='images',blank=True)
    image4=models.ImageField(upload_to='images',blank=True)
    catogery=models.ForeignKey(Catogery,on_delete=models.SET_NULL,null=True)
    ptype=models.ForeignKey(PriceType,on_delete=models.SET_NULL,null=True)
    btype=models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True)
    stocks=models.IntegerField(null=True)
    
    
    def __str__(self):
        return self.name