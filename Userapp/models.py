from django.db import models
from django.contrib.auth.models import AbstractUser
from Adminapp.models import *

# Create your models here.

class Users(AbstractUser):
    phone = models.CharField(max_length=11,null=True)
    adminstatus=models.BooleanField(blank=True,default=False,null=True)
    propic=models.ImageField(upload_to='images',blank=True,null=True)


AddType = (
    ("Home", "Home"),
    ("Work", "Work"),
)


class Address(models.Model):
	cust = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
	fname=models.CharField(max_length=30, null=True)
	lname=models.CharField(max_length=30,null=True)
	address = models.TextField(max_length=200, null=False)
	city = models.CharField(max_length=30, null=False)
	state = models.CharField(max_length=20, null=False)
	phone = models.CharField(max_length=11,null=True)
	pincode = models.IntegerField(null=False)
	type = models.CharField(
        max_length = 20,
        choices = AddType,
        default = '1'
        )

	def __str__(self):
		return self.address


PAYMENT_STATUS = (('Pending','Pending'),('Paid','Paid'))
STATUS = (
    ('New','New'),
    ('Pending','Pending'),
    ('Shipped','Shipped'),
    ('RequestedCancellation','RequestedCancellation'),
    ('Cancelled','Cancelled'),
    ('Delivered','Delivered'),
    ('RequestedReturn','RequestedReturn'),
    ('Return','Return'),
    )


class Order(models.Model):
	customer = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)
	address = models.ForeignKey(Address,on_delete=models.SET_NULL, null=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)
	status = models.CharField(max_length = 200,choices = STATUS, default = 'New', null=True)

	def __str__(self):
		return str(self.id)

	@property
	def get_cart_total(self):
		order_items = self.orderitem_set.all()
		total = sum([item.get_total for item in order_items])
		return total

	@property
	def get_cart_items(self):
		order_items = self.orderitem_set.all()
		total = sum([item.quantity for item in order_items])
		return total
		

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.product)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total



status_list = (
        ('None','None'),
        ('Completed','Completed'),
        ('Failed','Failed'),
    )

class Pay(models.Model):
    amount = models.CharField(max_length=30,default=0)
    method = models.CharField(max_length=30,)
    status = models.CharField(max_length=30, choices=status_list, default='None',)
    order =  models.OneToOneField(Order, on_delete=models.CASCADE)  
    transactionid = models.CharField(max_length= 100,null= True ,blank=True)





	
    

