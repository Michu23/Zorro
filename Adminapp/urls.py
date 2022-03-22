from django.urls import path
from . import views

urlpatterns = [
   path('adminhome/',views.adminhome,name='AdminHome'),
   path('adminorders/',views.adminorders,name='AdminOrders'),
   path('orderdetails/<str:pk>',views.adminorderdetail,name='AdminOrderDetail'),

   path('adminproduct/',views.adminproduct,name='AdminProduct'),
   path('adminproductna/',views.adminproductna,name='AdminProductna'),
   path('adminproductnd/',views.adminproductnd,name='AdminProductnd'),
   path('adminproductsa/',views.adminproductsa,name='AdminProductsa'),
   path('adminproductsd/',views.adminproductsd,name='AdminProductsd'),
   path('adminproductpa/',views.adminproductpa,name='AdminProductpa'),
   path('adminproductpd/',views.adminproductpd,name='AdminProductpd'),


   path('productoffer/',views.productoffer,name='ProductOffer'),
   path('applyoffer/',views.applyoffer,name='ApplyOffer'),

   path('filtercust/',views.filtercust,name='filtercust'),
   path('filterorder/',views.filterorder,name='filterorder'),
   path('filterpro/',views.filterpro,name='filterpro'),

   path('filter_shop',views.filter_shop, name="filter_shop"),


   path('',views.adminlogin,name='AdminLogin'),
   path('adminlogout',views.adminlogout,name='AdminLogout'),
   
   path('admincats/',views.admincats,name='AdminCats'),
   path('editcats/<str:pk>',views.editcats,name='EditCats'),
   path('delcats/<str:pk>',views.delcats,name='DelCats'),
   
   
   path('filterview/<str:id>',views.filterview,name='AFilterView'),
   path('filterbrand/<str:id>',views.filterbrand,name='AFilterBrand'),
   path('filterprice/<str:id>',views.filterprice,name='AFilterPrice'),
   
   path('customers/',views.admincustomers,name='AdminCustomers'),
   path('adminlogout/',views.adminlogout,name='AdminLogout'),
   path('editproduct/<str:pk>',views.editproduct,name='EditProduct'),
   path('deleteproduct/',views.deleteproduct,name='DeleteProduct'),
   path('salesreport/',views.salesreport,name='SalesReport'),
   # path('sales_report/',views.sales_report,name='Sales_Report'),
   path('addproduct/',views.addproduct,name='AddProduct'),
   path('blockuser',views.blockuser,name='blockuser'),
   
   path('acceptorder/<str:id>',views.acceptorder,name='acceptorder'),
   path('cancelorder/<str:id>',views.cancelorder,name='cancelorder'),
   path('deliverorder/<str:id>',views.deliverorder,name='deliverorder'),
   
   path('couponsused/',views.couponsused,name='couponsused'),
   path('admincoupons/',views.admincoupons,name='AdminCoupons'),
   path('editcoupons/<str:id>',views.editcoupons,name='EditCoupons'),
   path('deletecoupons/<str:id>',views.deletecoupons,name='DeleteCoupons'),

   path('export_csv/',views.export_csv,name="export_csv"),
   path('export_excel/',views.export_excel,name="export_excel"),

]