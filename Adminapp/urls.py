from django.urls import path
from . import views

urlpatterns = [
   path('adminhome/',views.adminhome,name='AdminHome'),
   path('adminorders/',views.adminorders,name='AdminOrders'),
   path('orderdetails/<str:pk>',views.adminorderdetail,name='AdminOrderDetail'),
   path('adminproduct/',views.adminproduct,name='AdminProduct'),
   
   path('filterview/<str:id>',views.filterview,name='AFilterView'),
   path('filterbrand/<str:id>',views.filterbrand,name='AFilterBrand'),
   path('filterprice/<str:id>',views.filterprice,name='AFilterPrice'),
   
   path('customers/',views.admincustomers,name='AdminCustomers'),
   path('',views.adminlogin,name='AdminLogin'),
   path('adminlogout/',views.adminlogout,name='AdminLogout'),
   path('editproduct/<str:pk>',views.editproduct,name='EditProduct'),
   path('deleteproduct/<str:pk>',views.deleteproduct,name='DeleteProduct'),
   path('invoice/',views.admininvoices,name='AdminInvoice'),
   path('addproduct/',views.addproduct,name='AddProduct'),
   path('blockuser/<str:pk>',views.blockuser,name='blockuser'),
   
]