from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse

from .forms import *
from .models import Product
from Userapp.models import *
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from Userapp.models import Users
from django.contrib import messages
from django.db.models import Count,Sum
from django.db.models import Q
from django.template.loader import render_to_string
from django.core.paginator import EmptyPage , PageNotAnInteger , Paginator
from django.conf import settings
import uuid
import xlwt
import datetime
from datetime import timedelta
import csv
import xlwt
# Create your views here.




@never_cache
def export_csv(request):
    order_data = Pay.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=SalesReport'+str(datetime.datetime.now())+'.csv'
    writer = csv.writer(response)   
    writer.writerow(['ID','Name','Number Of Products','Order Date','Amount','Payment Type'])
    for data in order_data:
        writer.writerow([data.id, data.order.customer, data.order.get_cart_items, data.order.date_ordered,data.amount , data.method])
    return response

@never_cache
def export_excel(request):
    order_data = Pay.objects.all()
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=SalesReport'+str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales Report')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['ID','Name','Order Date','Amount','Payment Type']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()

    rows = order_data.values_list(
        'order__id','order__customer__username','order__date_ordered','amount','method'
    )
    
    for row in rows:
        row_num = row_num + 1

        for col_num in range(len(columns)):
             ws.write(row_num,col_num,str(row[col_num]),font_style)
    wb.save(response)

    return response



def salesreport(request):
    order_data=Pay.objects.all().order_by('id')
    yr = []
    ag = 2000
    months = ['January', 'February', 'March','April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    for i in range(0,51):
        yr.append(ag + i)
    if request.method == 'POST':
        datestr = request.POST.get('dates')
            #start date
        mo = datestr[:2]
        da = datestr[3:5]
        ye = datestr[6:10]
        #enddate
        mo1 = datestr[13:15]
        da1 = datestr[16:18]
        ye1 = datestr[19:]
        from_date = ye+'-'+mo+'-'+da
        to_date = ye1+'-'+mo1+'-'+da1

        if from_date == "--" and to_date == "--":
            from_date = ''
            to_date = '' 
        

        year = request.POST.get('year')
        month = request.POST.get('month')
        print(month)
        print(from_date,to_date,"////////////////////////////////////////")
        m = month
        
        
        if  month != '' :
            order_data = Pay.objects.filter(order__date_ordered__month=m).order_by('order__date_ordered')
        elif  year != '' :
            order_data = Pay.objects.filter(order__date_ordered__year=year).order_by('order__date_ordered')
        elif from_date != '' and to_date != '' :
            order_data = Pay.objects.filter(order__date_ordered__range=[from_date,to_date]).order_by('order__date_ordered')

    context = {'years': yr,'months':months,'sales':'sales','pay':order_data}
    return render(request, "salesreport.html",context)


@never_cache
def adminsale(request):
    page = 'salesreport'
    global order_data
    order_data = OrderItem.objects.filter(order_payments_status='Completed')
    yr = []
    ag = 2000
    months = ['January', 'February', 'March','April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    for i in range(0,51):
        yr.append(ag + i)
    if request.method == 'POST':
        datestr = request.POST.get('dates')
            #start date
        mo = datestr[:2]
        da = datestr[3:5]
        ye = datestr[6:10]
        #enddate
        mo1 = datestr[13:15]
        da1 = datestr[16:18]
        ye1 = datestr[19:]
        from_date = ye+'-'+mo+'-'+da
        to_date = ye1+'-'+mo1+'-'+da1
        
        year = request.POST.get('year')
        month = request.POST.get('month')
        print(month)
        m = month
        print(m)
        print(from_date)
        if  month != '' :
            order_data = OrderItem.objects.filter(order_date_ordermonth=m).filter(orderpaymentsstatus='Completed').order_by('order_date_order')
        elif  year != '' :
            order_data = OrderItem.objects.filter(order_date_orderyear=year).filter(orderpaymentsstatus='Completed').order_by('order_date_order')
        elif from_date != '' and to_date != '' :
            order_data = OrderItem.objects.filter(order_date_orderrange=[from_date,to_date]).filter(orderpaymentsstatus='Completed').order_by('order_date_order')

    context = {'order_data': order_data, 'years': yr,'page': page,'months':months}
    return render(request,'adminsale3.html', context)


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


def adminlogout(request):
    logout(request)
    return redirect("AdminLogin")

@never_cache
def adminhome(request):
    
    products = Product.objects.all()
    
    placed = Order.objects.filter(status= 'Placed').count()
    shipped = Order.objects.filter(status= 'Shipped').count()
    completed = Order.objects.filter(status= 'Completed').count()
    cancelled = Order.objects.filter(status= 'Cancelled').count()
    out_of_delivery = Order.objects.filter(status= 'Delivered').count()
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
    paginator = Paginator (users, 6)
    page = request.GET.get('page')
    paged_users = paginator.get_page(page)
    context = {'users':paged_users,'cust':'cust'}
    return render(request, "customers.html",context)


@never_cache
def filtercust(request):
    print("//////////////////////////")
    user=request.user
    if 'cust' in request.GET:
        keyword = request.GET['cust']
        if keyword:
            cust = Users.objects.order_by('id').filter(Q(username__icontains=keyword) | Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword) | Q(phone__icontains=keyword) | Q(email__icontains=keyword)  )
            custcount = cust.count()

    else:
        messages.error(request,"No results found")
        return redirect("AdminCustomers")

    context = {'custcount':custcount,'users':cust}
    return render (request,'customers.html',context)


@never_cache
def filter_shop(request):
    print("///////////////////")
    print(request.GET)
    
    brands=request.GET.getlist('brands[]')
    categories = request.GET.getlist('catogery[]')
    ptype = request.GET.getlist('ptype[]')

    print(ptype)
    allProducts=Product.objects.all()
    if len(brands)>0:
        allProducts = allProducts.filter(btype__id__in=brands).distinct()
    if len(categories)>0:
        allProducts = allProducts.filter(catogery__id__in=categories).distinct()
    if len(ptype)>0:
        allProducts = allProducts.filter(ptype__id__in=ptype).distinct()
    
    t=render_to_string('filteredpro.html',{'productss':allProducts})  
    return JsonResponse({'data': t})


@never_cache
def filterorder(request):
    print("//////////////////////////")
    user=request.user
    if 'order' in request.GET:
        keyword = request.GET['order']
        if keyword:
            order = Order.objects.order_by('id').filter(Q(customer__username__icontains=keyword) | Q(address__address__icontains=keyword) | Q(date_ordered__icontains=keyword) | Q(status__icontains=keyword)  )
            ordercount = order.count()
        else:
            messages.error(request,"No results found")
            return redirect("AdminCustomers")

    context = {'ordercount':ordercount,'orders':order}
    return render (request,'order.html',context)


@never_cache
def filterpro(request):
    user=request.user
    if 'search' in request.GET:
        keyword = request.GET['search']
        if keyword:
            products = Product.objects.order_by('-price').filter( Q(description__icontains=keyword) | Q(name__icontains=keyword) | Q(catogery__name__icontains=keyword) | Q(btype__bname__icontains=keyword) | Q(ptype__genre__icontains=keyword) | Q(price__icontains=keyword)  )
            productcount = products.count()

        else:
            messages.error(request,"No results found")
            return redirect("UserShop")
    catogeries = Catogery.objects.all().annotate(numpro=Count('product'))
    brands=Brand.objects.all().annotate(bpro=Count('product'))
    ptypes=PriceType.objects.all().annotate(ppro=Count('product'))
    context = {'productss':products,'productcount':productcount,'catogeriess':catogeries,'brands':brands,'ptypes':ptypes,'pro':'pro'}
    return render (request,'productlist.html',context)





def adminorders(request):
    orders=Order.objects.filter(complete=True).order_by('-date_ordered')
    paginator = Paginator (orders, 4)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)
    context={'orders':paged_orders,'abc':'abc'}
    return render(request, "order.html",context)

def adminordersa(request):
    orders=Order.objects.filter(complete=True).order_by('date_ordered')
    paginator = Paginator (orders, 4)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)
    context={'orders':paged_orders,'abc':'abc'}
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

def deleteproduct(request):
    pk=request.GET.get('productid')
    product = Product.objects.get(id=pk)
    product.delete()
    response={'':''}
    return JsonResponse(response)
    
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
    products = Product.objects.all()
    paginator = Paginator (products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    productcount=products.count()
    catogeries = Catogery.objects.all().annotate(numpro=Count('product'))
    brands=Brand.objects.all().annotate(bpro=Count('product'))
    ptypes=PriceType.objects.all().annotate(ppro=Count('product'))
    context = {'productss':paged_products,'catogeriess':catogeries,'brands':brands,'ptypes':ptypes,'pro':'pro'}
    return render(request, "productlist.html",context)



def adminproductna(request):
    products = Product.objects.all().order_by('name')
    paginator = Paginator (products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    productcount=products.count()
    catogeries = Catogery.objects.all().annotate(numpro=Count('product'))
    brands=Brand.objects.all().annotate(bpro=Count('product'))
    ptypes=PriceType.objects.all().annotate(ppro=Count('product'))
    context = {'productss':paged_products,'catogeriess':catogeries,'brands':brands,'ptypes':ptypes,'pro':'pro'}
    return render(request, "productlist.html",context)



def adminproductnd(request):
    products = Product.objects.all().order_by('-name')
    paginator = Paginator (products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    productcount=products.count()
    catogeries = Catogery.objects.all().annotate(numpro=Count('product'))
    brands=Brand.objects.all().annotate(bpro=Count('product'))
    ptypes=PriceType.objects.all().annotate(ppro=Count('product'))
    context = {'productss':paged_products,'catogeriess':catogeries,'brands':brands,'ptypes':ptypes,'pro':'pro'}
    return render(request, "productlist.html",context)



def adminproductpa(request):
    products = Product.objects.all().order_by('price')
    paginator = Paginator (products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    productcount=products.count()
    catogeries = Catogery.objects.all().annotate(numpro=Count('product'))
    brands=Brand.objects.all().annotate(bpro=Count('product'))
    ptypes=PriceType.objects.all().annotate(ppro=Count('product'))
    context = {'productss':paged_products,'catogeriess':catogeries,'brands':brands,'ptypes':ptypes,'pro':'pro'}
    return render(request, "productlist.html",context)



def adminproductpd(request):
    products = Product.objects.all().order_by('-price')
    paginator = Paginator (products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    productcount=products.count()
    catogeries = Catogery.objects.all().annotate(numpro=Count('product'))
    brands=Brand.objects.all().annotate(bpro=Count('product'))
    ptypes=PriceType.objects.all().annotate(ppro=Count('product'))
    context = {'productss':paged_products,'catogeriess':catogeries,'brands':brands,'ptypes':ptypes,'pro':'pro'}
    return render(request, "productlist.html",context)



def adminproductsa(request):
    products = Product.objects.all().order_by('stocks')
    paginator = Paginator (products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    productcount=products.count()
    catogeries = Catogery.objects.all().annotate(numpro=Count('product'))
    brands=Brand.objects.all().annotate(bpro=Count('product'))
    ptypes=PriceType.objects.all().annotate(ppro=Count('product'))
    context = {'productss':paged_products,'catogeriess':catogeries,'brands':brands,'ptypes':ptypes,'pro':'pro'}
    return render(request, "productlist.html",context)



def adminproductsd(request):
    products = Product.objects.all().order_by('-stocks')
    paginator = Paginator (products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    productcount=products.count()
    catogeries = Catogery.objects.all().annotate(numpro=Count('product'))
    brands=Brand.objects.all().annotate(bpro=Count('product'))
    ptypes=PriceType.objects.all().annotate(ppro=Count('product'))
    context = {'productss':paged_products,'catogeriess':catogeries,'brands':brands,'ptypes':ptypes,'pro':'pro'}
    return render(request, "productlist.html",context)





def productoffer(request):
    products = Product.objects.all().order_by('-price')
    context = {'products':products,'offerpro':'offerpro'}
    return render(request, "productoffer.html",context)

def applyoffer(request):
    pk=request.GET.get('productid')
    product = Product.objects.get(id=pk)
    if product.offer == False:
        product.offer=True
    else:
        product.offer=False
    status=product.offer
    product.save()
    status={'status':status}
    return JsonResponse(status)

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





def addproduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Product is Added')
            return redirect('AddProduct')
        else:
            messages.error(request,'Invalid Form')
            return render(request,'addproduct.html',{'form':form})

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
    brands=Brand.objects.all()
    cats=Catogery.objects.all()
    form= MyCatForm()
    if request.method == 'POST':
        form = MyCatForm(request.POST)
        if form.is_valid():
            form.save()
            messages.error(request,"Successfully added")
            return redirect("AdminCats")
        else:
            messages.error(request,"Error")
    context={'form':form,'cats':cats,'brands':brands}
    return render (request, "cats.html",context)

def editcats(request,pk):
    page="edit"
    cats = Catogery.objects.get(id=pk)
    formm = MyCatForm(instance=cats)
    if request.method == 'POST': 
        formm = MyCatForm(request.POST,instance=cats)
        if formm.is_valid():
            formm.save()
            messages.success(request,'Updated Successfully')
            return redirect('AdminCats')
        else:
            messages.error(request,'Form is not valid')
            print(formm.errors)
    return render(request,'cats.html',{'formm':formm,'page':page})

def delcats(request,pk):
    cats = Catogery.objects.get(id=pk)
    cats.delete()
    return redirect("AdminCats")



def couponsused(request):
    coupons = CouponUsed.objects.filter(applied=True)
    context={'coupons': coupons}
    return render(request,'couponused.html',context)


def admincoupons(request):
    coupons= CouponDetail.objects.all()
    couponform= MyCouponForm()
    if request.method == 'POST':
        couponform = MyCouponForm(request.POST)
        if couponform.is_valid():
            couponform.save()
            messages.success(request,"Successfully added")
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




    







