from django.urls import path,include
from . import views

urlpatterns = [
   path('',views.userhome,name='UserHome'),
   path('reg/',views.userreg,name='UserReg'),
   path('checkout/',views.usercheckout,name='UserCheckout'),
   path('cart/',views.usercart,name='UserCart'),
   path('shop/',views.usershop,name='UserShop'),
   path('filterview/<str:id>',views.filterview,name='FilterView'),
   path('filterbrand/<str:id>',views.filterbrand,name='FilterBrand'),
   path('filterprice/<str:id>',views.filterprice,name='FilterPrice'),
   # path('filter-data',views.filter-data,name="filter-data"),
   path('login/',views.userlogin,name='UserLogin'),
   path('logout/',views.userlogout,name='UserLogout'),
   path('remove/', views.remove, name='Remove'),
   path('profiledash/',views.profiledash,name='ProfileDash'),
   path('address/',views.address,name='UserAddress'),
   path('editaddress/<str:pk>',views.editaddress,name='EditUserAddress'),
   path('deleteaddress/<str:pk>',views.deleteaddress,name='DeleteUserAddress'),
   path('orders/',views.profileorder,name='UserOrders'),
   path('cancelorder/<str:id>',views.cancelorder,name="cancelorder"),
   path('returnorder/<str:id>',views.returnorder,name="returnorder"),
   path('wishlist/',views.wishlist,name='Wishlist'),
   path('product/<str:pk>',views.product,name='Product'),
   path('otplogin/',views.otplogin,name='OtpLogin'),
   path('otpverify/',views.otpverify,name='OtpVerify'),
   path('proceed/', views.proceed, name='proceed'),
   path('updateitem/', views.updateitem, name='updateitem'),
   path('editprofile/', views.editprofile, name='editprofile'),
   path('razorpay/',views.razorpay,name='razorpay'),
   path('payrazor/',views.payrazor,name='payrazor'),
   path('paypal/',views.paypal,name='paypal'),
   
   
   
   
   
   # path('updatecart/', views.updatecart, name='updatecart'),
   
   
]