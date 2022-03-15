from django.db import models
from django.contrib.auth.models import AbstractUser
from babel.numbers import format_currency
from Adminapp.models import *

# Create your models here.

class Users(AbstractUser):
	phone = models.CharField(max_length=11,null=True)
	adminstatus=models.BooleanField(blank=True,default=False,null=True)
	propic=models.ImageField(upload_to='images',default="2950f96af23e53d8ba98351184c2c803_eW7MOkE.jpg" ,blank=True,null=True)
	device = models.CharField( max_length=60 , null=True , blank=True )
	
def __str__(self):
		if self.username=="":
			return self.device
		else:
			return self.username
	


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
    ('BuyNow','BuyNow'),
    ('New','New'),
    ('Placed','Placed'),
    ('Cancelled','Cancelled'),
    ('Shipped','Shipped'),
    ('Delivered','Delivered'),
    ('Return','Return'),
    ('RequestedReturn','RequestedReturn'),
    )

OFFERS = (
    ('None','None'),
    ('ProductOffer','ProductOffer'),
    ('CatogeryOffer','CatogeryOffer'),
    )

class Order(models.Model):
	customer = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)
	address = models.ForeignKey(Address,on_delete=models.SET_NULL, null=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	status = models.CharField(max_length = 200,choices = STATUS, default = 'New', null=True)
	coupon_used=models.BooleanField(default=False, null=True , blank=True )
	offer_used= models.CharField(max_length = 50,choices = OFFERS, default = 'None', null=True)

	def __str__(self):
		return str(self.complete)

	
	@property
	def get_cart_total(self):
		order_items = self.orderitem_set.all()
		total = sum([item.gettotal for item in order_items])
		if self.coupon_used== False:
			return total
		else :
			total = total - self.couponused.loss
			return total

	@property
	def get_cart_oldtotal(self):
		order_items = self.orderitem_set.all()
		total = sum([item.getoldtotal for item in order_items])
		return total

	@property
	def get_cart_totall(self):
		total = self.get_cart_total
		totalinr = format_currency(total, 'INR', locale='en_IN')
		return totalinr

	@property
	def get_cart_oldtotall(self):
		total = self.get_cart_oldtotal
		totalinr = format_currency(total, 'INR', locale='en_IN')
		return totalinr

	
		
 
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
	def gettotal(self):
		total = self.product.newprice * self.quantity
		return total

	@property
	def getoldtotal(self):
		total = self.product.price * self.quantity
		return total
	

	@property
	def get_total(self):
		total = self.product.newprice * self.quantity
		totalinr = format_currency(total, 'INR', locale='en_IN')
		return totalinr

	

status_list = (
        ('None','None'),
        ('Completed','Completed'),
        ('Failed','Failed'),
    )

class Pay(models.Model):
	payuser = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)
	amount = models.FloatField()
	method = models.CharField(max_length=30)
	status = models.CharField(max_length=30, choices=status_list, default='None')
	order =  models.OneToOneField(Order, on_delete=models.CASCADE)  
	transactionid = models.CharField(max_length= 100,null= True ,blank=True)
    
	def __str__(self):
		return str(self.amount)

class CouponDetail(models.Model):
    name = models.CharField(max_length=30,null= True, blank=True)
    code = models.CharField(max_length=30)
    percentage = models.FloatField(max_length=30,default=0)
    created = models.DateField(auto_now_add=True)
    expdate = models.DateField(null=True, blank=True)
    count= models.FloatField(max_length=30,default=0)
    loss = models.FloatField(max_length=30,default=0)
    active = models.BooleanField(default=True,null=True)
    

    def __str__(self):
        return self.name

    @property
    def lossinr(self):
        total = self.loss
        totalinr = format_currency(total, 'INR', locale='en_IN')
        return totalinr


class CouponUsed(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True) 
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True)
    coupon = models.ForeignKey(CouponDetail, on_delete=models.CASCADE, blank=True, null=True)
    used = models.BooleanField(default=False)
    loss = models.FloatField(max_length=30,default=0)
    applied = models.BooleanField(default=False,null=True,blank=True)
	
    def __str__(self):
        return self.coupon.code		

    @property
    def lossinr(self):
        total = self.loss
        totalinr = format_currency(total, 'INR', locale='en_IN')
        return totalinr


class Wishlist(models.Model):
	useradded=models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True) 
	productadded=models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.useradded.username

		
