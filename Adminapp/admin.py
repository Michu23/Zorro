from django.contrib import admin
from Userapp.models import *
from Adminapp.models import *

# Register your models here.

admin.site.register(Product)
admin.site.register(Catogery)
admin.site.register(Users)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Pay)
admin.site.register(PriceType)
admin.site.register(Brand)
admin.site.register(CouponDetail)
admin.site.register(CouponUsed)
admin.site.register(Wishlist)

