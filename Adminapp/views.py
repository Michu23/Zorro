from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import ProductForm
from .models import Product
from Userapp.models import *
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from Userapp.models import Users
from django.contrib import messages
from django.db.models import Count




# Create your views here.
@never_cache
def adminlogin(request):
    if request.user.is_authenticated:
        return redirect('AdminHome')
    if request.method == 'POST':
        admin = request.POST.get('username')
        password = request.POST.get('password')
        if admin == 'supermichu' and password == 'django':
            try:
                user=authenticate(username=admin,password=password)
            except:
                print("Hello")
            if user is not None:
                login(request,user)
                return redirect('AdminHome')
            else:
                messages.error(request,'You are not Admin')
    return render (request,"adminlogin.html")

@never_cache
@login_required(login_url='adminlogin')
def adminhome(request):
    return render(request, "adminindex.html",{'dashboard':'dashboard'})

@never_cache
def adminlogout(request):
    logout(request)
    return redirect('AdminLogin')

def admincustomers(request):
    users = Users.objects.all()
    context = {'users':users,'cust':'cust'}
    return render(request, "customers.html",context)

def adminorders(request):
    orders=Order.objects.filter(complete=True)
    context={'orders':orders}
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
        form = ProductForm(request.POST,instance=product)
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
@login_required(login_url='admin-login')
def blockuser(request,pk):
    print("Are you thereeee")
    user = Users.objects.get(id=pk)
    if user.adminstatus == False:
        Users.adminstatus=True
    else:
        Users.adminstatus=False
    user.save()
    return redirect("AdminCustomers")

def adminproduct(request):
    products = Product.objects.all()
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
    return render(request, "shop.html",context)

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
    return render(request, "shop.html",context)

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
    return render(request, "shop.html",context)


def admininvoices(request):
    return render(request, "invoices.html",{'invoices':'invoices'})

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


    







