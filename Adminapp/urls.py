from django.urls import path
from . import views

urlpatterns = [
   path('adminhome/',views.adminhome,name='AdminHome'),
   path('adminorders/',views.adminorders,name='AdminOrders'),
   path('orderdetails/<str:pk>',views.adminorderdetail,name='AdminOrderDetail'),
   path('adminproduct/',views.adminproduct,name='AdminProduct'),
   path('',views.adminlogin,name='AdminLogin'),
   
   path('admincats/',views.admincats,name='AdminCats'),
   path('editcats/<str:pk>',views.editcats,name='EditCats'),
   path('delcats/<str:pk>',views.delcats,name='DelCats'),
   
   # path('adminbrands/',views.adminbrands,name='Adminbrands'),
   # path('addbrands/<str:pk>',views.addbrands,name='Addbrands'),
   # path('delbrands/<str:pk>',views.delbrands,name='Delbrands'),
   
   path('filterview/<str:id>',views.filterview,name='AFilterView'),
   path('filterbrand/<str:id>',views.filterbrand,name='AFilterBrand'),
   path('filterprice/<str:id>',views.filterprice,name='AFilterPrice'),
   
   path('customers/',views.admincustomers,name='AdminCustomers'),
   path('adminlogout/',views.adminlogout,name='AdminLogout'),
   path('editproduct/<str:pk>',views.editproduct,name='EditProduct'),
   path('deleteproduct/<str:pk>',views.deleteproduct,name='DeleteProduct'),
   path('salesreport/',views.salesreport,name='SalesReport'),
   path('addproduct/',views.addproduct,name='AddProduct'),
   path('blockuser',views.blockuser,name='blockuser'),
   
   path('acceptorder/<str:id>',views.acceptorder,name='acceptorder'),
   path('cancelorder/<str:id>',views.cancelorder,name='cancelorder'),
   path('deliverorder/<str:id>',views.deliverorder,name='deliverorder'),
   
   path('couponsused/',views.couponsused,name='couponsused'),
   path('admincoupons/',views.admincoupons,name='AdminCoupons'),
   path('editcoupons/<str:id>',views.editcoupons,name='EditCoupons'),
   path('deletecoupons/<str:id>',views.deletecoupons,name='DeleteCoupons'),
   
]