from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
   path('',views.userhome,name='UserHome'),
   path('reg/',views.userreg,name='UserReg'),
   path('signupotp/',views.signupotp,name="SignupOtp"),
   path('signupotpverify/',views.signupotpverify,name="SignupOtpVerify"),
   
   path('checkout/',views.usercheckout,name='UserCheckout'),
   path('cart/',views.usercart,name='UserCart'),
   path('shop/',views.usershop,name='UserShop'),
   path('buynow/<str:id>',views.buynow,name='BuyNow'),
   path('filterview/<str:id>',views.filterview,name='FilterView'),
   path('filterbrand/<str:id>',views.filterbrand,name='FilterBrand'),
   path('filterprice/<str:id>',views.filterprice,name='FilterPrice'),
   # path('filter-data',views.filter-data,name="filter-data"),
   path('login/',views.userlogin,name='UserLogin'),
   path('logout/',views.userlogout,name='UserLogout'),
   path('remove/', views.remove, name='Remove'),

   path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"),
   path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
   path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


   path('profiledash/',views.profiledash,name='ProfileDash'),
   path('address/',views.address,name='UserAddress'),
   path('editaddress/<str:pk>',views.editaddress,name='EditUserAddress'),
   path('deleteaddress/<str:pk>',views.deleteaddress,name='DeleteUserAddress'),
   path('orders/',views.profileorder,name='UserOrders'),
   path('orderdetails/<str:id>',views.profileorderdetails,name='UserOrderDeatils'),
   path('cancelorder/<str:id>',views.cancelorder,name="usercancelorder"),
   path('returnorder/<str:id>',views.returnorder,name="userreturnorder"),
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
   path('verifycoupon/',views.verifycoupon,name='verifycoupon'),
   
   path('invoicedetails/',views.invoicedetails,name='invoicedetails'),
   path('wishlist/',views.wishlist,name="wishlist"),
   # path('updatecart/', views.updatecart, name='updatecart'),
   
   
]