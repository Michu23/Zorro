from django.db import models
from django.contrib.auth.models import AbstractUser
from babel.numbers import format_currency
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Catogery(models.Model):
    name=models.CharField(max_length=100,null=True)
    catoffer= models.BooleanField(null=True,blank=True,default=False)
    catpercent= models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)],null=True,blank=True,default=5)
    
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
    price=models.FloatField(validators=[MinValueValidator(0)],null=True)
    image1=models.ImageField(upload_to='images',blank=True)
    image2=models.ImageField(upload_to='images',blank=True)
    image3=models.ImageField(upload_to='images',blank=True)
    image4=models.ImageField(upload_to='images',blank=True)
    catogery=models.ForeignKey(Catogery,on_delete=models.SET_NULL,null=True)
    ptype=models.ForeignKey(PriceType,on_delete=models.SET_NULL,null=True)
    btype=models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True)
    stocks=models.IntegerField(validators=[MinValueValidator(0)],null=True)
    offer=models.BooleanField(null=True,blank=True,default=False)
    offerpercent=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)],null=True,blank=True,default=5)
    offerbuycount=models.BooleanField(null=True,blank=True,default=0)



    @property
    def newprice(self):
        offerp = self.price
        productoffer = self.offerpercent
        catoffer = self.catogery.catpercent
        if self.offer==True and self.catogery.catoffer==False:
            offerp = self.price - ((self.price)*(self.offerpercent/100))
            return offerp
        elif self.offer==False and self.catogery.catoffer==True:
            offerp = self.price - ((self.price)*(self.catogery.catpercent/100))
            return offerp
        elif self.offer==True and self.catogery.catoffer==True:
            if self.catogery.catpercent > self.offerpercent:
                offerp = self.price - ((self.price)*(self.catogery.catpercent/100))
                return offerp
            elif self.catogery.catpercent < self.offerpercent:
                offerp = self.price - ((self.price)*(self.offerpercent/100))
                return offerp
            else:
                offerp = self.price - ((self.price)*(self.offerpercent/100))
                return offerp
        else:
            return offerp

    @property
    def offerused(self):
        offerp = self.price
        productoffer = self.offerpercent
        catoffer = self.catogery.catpercent
        if self.offer==True and self.catogery.catoffer==False:
            return str("productoffer")
        elif self.offer==False and self.catogery.catoffer==True:
            return str("catoffer")
        elif self.offer==True and self.catogery.catoffer==True:
            if self.catogery.catpercent > self.offerpercent:
                return str("catoffer")
            elif self.catogery.catpercent < self.offerpercent:
                return str("productoffer")
            else:
                return str("productoffer")

        else:
            return str("Not used")


    @property
    def newpriceinr(self):
        total=self.newprice
        totalinr = format_currency(total, 'INR', locale='en_IN')
        return totalinr

    
    def __str__(self):
        return self.name
    
    @property
    def priceinr(self):
        total=self.price
        totalinr = format_currency(total, 'INR', locale='en_IN')
        return totalinr