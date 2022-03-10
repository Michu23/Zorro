from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from .models import Product
from Userapp.models import *
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from Userapp.models import Users
from django.contrib import messages
from django.db.models import Count,Sum
from datetime import datetime,date,timedelta
import xlwt
import csv
import datetime





# Create your views here.
@never_cache
def adminlogin(request):
    if request.user.is_authenticated:
        return redirect('AdminHome')
    if request.method == 'POST':
        admin = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user=authenticate(username=admin,password=password)
        except:
            print("Hello")
        if user is not None:    
            if user.is_staff==True:
                login(request,user)
                return redirect('AdminHome')
            else:
                messages.error(request,"You're not an admin")
        else:
            messages.error(request,"Invalid details")
    return render (request,"adminlogin.html")

@never_cache
def adminhome(request):
    
    products = Product.objects.all()
    
    placed = Order.objects.filter(status= 'Placed').count()
    shipped = Order.objects.filter(status= 'Shipped').count()
    completed = Order.objects.filter(status= 'Delivered').count()
    cancelled = Order.objects.filter(status= 'Cancelled').count()
    out_of_delivery = Order.objects.filter(status= 'Out Of Delevery').count()
    returned = Order.objects.filter(status= 'Return').count()
    order_status = [placed,shipped,out_of_delivery,completed,cancelled,returned]

    cod = Pay.objects.filter(method = 'COD').count()
    paypal = Pay.objects.filter(method = 'Paypal').count()
    razorpay = Pay.objects.filter(method = 'RazorPay').count()
    payment_type = [cod,paypal,razorpay]
    
    orderitems = Order.objects.filter(complete= True)
    print(orderitems)
    
    customers = Users.objects.all().count()
    orders = Order.objects.all().count()
    product_count = Product.objects.all().count()
    total_revenue = Pay.objects.all().aggregate(Sum('amount'))
    
    print(total_revenue)
    print(product_count)
    print(orders)
    print(customers)
    
    context = {'products':products,'order_status': order_status, 'payment_type': payment_type, 
     'customers':customers,'orders': orders, 'product_count':product_count,'dashboard':'dashboard','total_revenue':total_revenue}
    
    return render(request, "adminindex.html",context)

@never_cache
def adminlogout(request):
    logout(request)
    return redirect('AdminLogin')

def admincustomers(request):
    users = Users.objects.all().order_by('id')
    context = {'users':users,'cust':'cust'}
    return render(request, "customers.html",context)

def adminorders(request):
    orders=Order.objects.filter(complete=True).order_by('-date_ordered')
    context={'orders':orders,'abc':'abc'}
    return render(request, "order.html",context)

def adminorderdetail(request,pk):
    user= request.user
    order = Order.objects.get(id=pk)
    items=order.orderitem_set.all()
    context = {'order':order,'items':items,'details':'details'}
    return render(request, "orderdetails.html",context)

def editproduct(request,pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            messages.success(request,'Update Successfully')
            return redirect('AdminProduct')
    return render(request,'editproduct.html',{'form':form})

def deleteproduct(request,pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect("AdminProduct")
    
@never_cache
def blockuser(request):
    pk=request.GET.get('productid')
    user = Users.objects.get(id=pk)
    if user.adminstatus == False:
        user.adminstatus=True
    else:
        user.adminstatus=False
    user.save()
    return redirect("AdminCustomers")

def adminproduct(request):
    products = Product.objects.all().order_by('-price')
    catogeries = Catogery.objects.all().annotate(numpro=Count('product'))
    brands=Brand.objects.all().annotate(bpro=Count('product'))
    ptypes=PriceType.objects.all().annotate(ppro=Count('product'))
    context = {'products':products,'catogeries':catogeries,'brands':brands,'ptypes':ptypes,'pro':'pro'}
    return render(request, "productlist.html",context)

@never_cache
def filterview(request,id):
    catogery=Catogery.objects.all()
    catogeries = Catogery.objects.all().annotate(numpro=Count('product'))
    brand=Brand.objects.all()
    brands=Brand.objects.all().annotate(bpro=Count('product'))
    ptype=PriceType.objects.all()
    ptypes=PriceType.objects.all().annotate(ppro=Count('product'))
    products = Product.objects.filter(catogery=id)
    context = {'products':products,'catogeries':catogeries,'brands':brands,'ptypes':ptypes,'pro':'pro'}
    return render(request, "productlist.html",context)

@never_cache
def filterbrand(request,id):
    catogery=Catogery.objects.all()
    catogeries = Catogery.objects.all().annotate(numpro=Count('product'))
    brand=Brand.objects.all()
    brands=Brand.objects.all().annotate(bpro=Count('product'))
    ptype=PriceType.objects.all()
    ptypes=PriceType.objects.all().annotate(ppro=Count('product'))
    products = Product.objects.filter(btype=id)
    context = {'products':products,'catogeries':catogeries,'brands':brands,'ptypes':ptypes}
    return render(request, "productlist.html",context)

@never_cache
def filterprice(request,id):
    catogery=Catogery.objects.all()
    catogeries = Catogery.objects.all().annotate(numpro=Count('product'))
    ptype=PriceType.objects.all()
    ptypes = PriceType.objects.all().annotate(ppro=Count('product'))
    brand=Brand.objects.all()
    brands=Brand.objects.all().annotate(bpro=Count('product'))
    products = Product.objects.filter(ptype=id)
    context = {'products':products,'catogeries':catogeries,'brands':brands,'ptypes':ptypes}
    return render(request, "productlist.html",context)


def salesreport(request):
    pay=Pay.objects.all()
    context={'sales':'sales','pay':pay}
    return render(request, "salesreport.html",context)


def addproduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Product is Added')
            return redirect('AddProduct')
        else:
            form.errors
    else:
        return render(request,'addproduct.html',{'form':form})
    return render(request,'addproduct.html')


def acceptorder(request, id):
    order = Order.objects.get(id = id)
    items = OrderItem.objects.filter(order = order)
    order.status = 'Shipped'
    order.save()
    return redirect('AdminOrders')

def deliverorder(request, id):
    order = Order.objects.get(id = id)
    items = OrderItem.objects.filter(order = order)
    order.status = 'Delivered'
    order.save()
    return redirect('AdminOrders')


def cancelorder(request, id):
    order = Order.objects.get(id = id)
    items = OrderItem.objects.filter(order = order)
    order.status = 'Cancelled'
    for item in items :
        ordered = item.quantity
        stock = item.quantity
        newstock = stock + ordered
        productid = item.product.id
        Product.objects.filter(id = productid).update(stocks = newstock)
    order.save()
    return redirect('AdminOrders')


def admincats(request):
    # brands=Brand.objects.all()
    # cats=Catogery.objects.all()
    # form= MyCatForm()
    # if request.method == 'POST':
    #     form = MyCatForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.error(request,"Successfully added")
    #         return redirect("AdminCats")
    #     else:
    #         messages.error(request,"Error")
    # context={'form':form,'cats':cats,'brands':brands}
    return render (request, "catogeries.html",context)

def addcats(request,pk):
    # page="edit"
    # cats = Catogery.objects.get(id=pk)
    # form = MyCatForm(instance=cats)
    # if request.method == 'POST': 
    #     form = MyCatForm(request.POST,instance=cats)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request,'Updated Successfully')
    #         return redirect('AdminCats')
    # formm= MyCatForm()
    # if request.method == 'POST':
    #     formm = MyCatForm(request.POST)
    #     if formm.is_valid():
    #         formm.save()
    #         messages.error(request,"Successfully added")
    #         return redirect("AdminCats")
    #     else:
    #         messages.error(request,"Error")
    return render(request,'catogeries.html',{'form':form,'formm':formm,'page':page})

def delcats(request,pk):
    # cats = Catogery.objects.get(id=pk)
    # cats.delete()
    return redirect("AdminCats")

# def adminbrands(request):
#     brands=Brand.objects.all()
#     cats=Catogery.objects.all()
#     form= MyCatForm()
#     if request.method == 'POST':
#         form = MyCatForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.error(request,"Successfully added")
#             return redirect("AdminCats")
#         else:
#             messages.error(request,"Error")
#     context={'form':form,'cats':cats,'brands':brands,'page':page}
#     return render (request, "catogeries.html",context)

# def addbrands(request,pk):
#     page="editbrand"
#     cats=Catogery.objects.all()
#     brands = Brand.objects.get(id=pk)
#     form = MyBrandForm(instance=brands)
#     if request.method == 'POST': 
#         form = MyBrandForm(request.POST,instance=brands)
#         if form.is_valid():
#             form.save()
#             messages.success(request,'Updated Successfully')
#             return redirect('AdminCats')
#     return render(request,'catogeries.html',{'form':form,'page':page,'cats':cats})

# def delbrands(request,pk):
#     brands = Brand.objects.get(id=pk)
#     brands.delete()
#     return redirect("AdminCats")


def couponsused(request):
    coupons = CouponUsed.objects.all()
    context={'coupons': coupons}
    return render(request,'couponused.html',context)

def admincoupons(request):
    coupons= CouponDetail.objects.all()
    couponform= MyCouponForm()
    if request.method == 'POST':
        couponform = MyCouponForm(request.POST)
        if couponform.is_valid():
            couponform.save()
            messages.error(request,"Successfully added")
            return redirect("AdminCoupons")
        else:
            messages.error(request,"Error")
    context= {'coupons':coupons,'couponform':couponform}
    return render (request, 'coupons.html',context)

def editcoupons(request,id):
    print("/////////////////////hi")
    coup = CouponDetail.objects.get(id=id)
    form = MyCouponForm(instance=coup)
    if request.method == 'POST': 
        print("/////////////////////hi")
        form = MyCouponForm(request.POST,instance=coup)
        if form.is_valid():
            form.save()
            messages.success(request,'Updated Successfully')
            return redirect('AdminCoupons')
        else:
            messages.error(request,"Error")
    context={'form':form,'coup':coup}
    return render(request,'editcoupon.html',context)

def deletecoupons(request,id):
    return render(request,'coupons.html') 


# def export_csv(request):
#     response['Content-Disposition'] = 'attachment; filename=Expenses' + \
#         str(datetime.datetime.now())+'.csv'
#     writer = csv.writer(response)
#     writer.writerow(['Amount', 'Description', 'Category', 'Date'])
#     expenses = Expense.objects.filter(owner=request.user)

#     for expense in expenses:
#         writer.writerow( [expense.amount, expense.description,
#                              expense.category, expense.date])
#     return response 

    
# def export_excel(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response ['Content-Disposition'] = 'attachment; filename-Expenses' +\
#         str(datetime, datetime.now())+'.xls'
#     wb = xlwt.Workbjiok(encoding='utf-8')
#     ws.add_sheet('Expenses')
                                           
#     row_num = 0
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
#     columns = ['ID', 'Description', 'Category', 'Date']
#     for col_num in range (len(columns) ):
#         ws.write(row_num, col_num, columns (col_num), font_style)
#     font_style = xlwt.XFStyle()
#     rows = Expense.objects.filter(owner=request.user).values_list(
#         'amount','description', 'category', 'date')

#     for row in rows:
#         row_num += 1
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, str(row[col_num]), font_style)

#     wb.save(response)
#     return response




@never_cache
def export_csv(request):
    global order_data
    order_data = Pay.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=SalesReport'+str(datetime.datetime.now())+'.csv'
    writer = csv.writer(response)   
    writer.writerow(['Id','Name','Payment','Items','Amount','Date and Time'])
    for data in order_data:
        writer.writerow([data.order.id, data.order.customer.username, data.method, data.order.get_cart_items,data.order.get_cart_totall , data.order.date_ordered])
    return response

@never_cache
def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=SalesReport'+str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales Report')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Id','Name','Payment','Items','Amount','Date and Time']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows = order_data.values_list(
        'id','order_customer','order_date','payment_total_amount','payment_payment_method'
    )
    for row in rows:
        row_num = row_num + 1

        for col_num in range(len(columns)):
             ws.write(row_num,col_num,str(row[col_num]),font_style)

    wb.save(response)
    return response



    







