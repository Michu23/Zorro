from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from .models import *
from Adminapp.models import *
from .forms import *
from django.contrib import messages
from twilio.rest import Client 
import random
from django.db.models import Count
from django.http import JsonResponse
from decouple import config
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@never_cache
def userlogin(request):
    if request.user.is_authenticated:
        return redirect('UserHome')
    if request.method == "POST":
        uname = request.POST.get('username')
        password= request.POST.get('password')
        try:
            user = Users.object.get(username=uname)
        except:
            messages.error(request,'User does not exists')
        
        try:
            user= authenticate(request,username=uname,password=password)
            if user.adminstatus == False:
                if user is not None:
                    login(request,user)
                    return redirect ("UserHome")   
            else:
                messages.error(request,"You have been banned by the admin. Please call our customer care for more details!")
        except:
            messages.error(request,'Invalid Password')
            
    return render(request, "login.html")


@never_cache
def userreg(request):
    form= MyUserFormUser()
    if request.method == 'POST':
        form = MyUserFormUser(request.POST)
        uname=request.POST.get("username")
        print(uname)
        umail=request.POST.get("email")
        uphone=request.POST.get("phone")
        un="Not taken"
        um="Not taken"
        up="Not taken"
        
        try:
            un = Users.object.get(username=uname)
            print(un)
            messages.error(request,"Username already taken")
        except:
            pass
        
        try:
            um = Users.object.get(email=umail)
            messages.error(request,"Email already taken")
        except:
            pass
        
        try:
            up = Users.object.get(phone=uphone)
            messages.error(request,"Phone number already taken")
        except:
            pass
        
        if un == "Not taken":
            if(len(str(uphone))<=10):
                if form.is_valid():
                    
                    
                    
                    
                    
                    
                    
                    user=form.save()
                    login(request,user)
                    return redirect("UserHome")
                else:
                    messages.error(request,"Enter the details properly!")
            else:
                messages.error(request,"Enter a 10 digit-number!")
        else:
            messages.error(request,"Username , email or phone already taken")
                
        
    context={'form':form}
    return render(request, "reg.html",context)


@never_cache
def otplogin(request):
    global number,phone
    if request.method == 'POST':
        phone = request.POST.get('number')
        number = '+91' + str(phone)
        user = None
        try:
            user = Users.objects.get(phone=phone)
        except:
            messages.error(request,"No matching phone number found!")
            return render(request, 'otplogin.html') 
        if user is not None:
            account_sid = config('account_sid')
            auth_token = config('auth_token')
            client = Client(account_sid, auth_token)
            verification = client.verify \
                                .services(config('services')) \
                                .verifications \
                                .create(to=number, channel='sms')
            return redirect ('OtpVerify')
    return render(request,'otplogin.html')


@never_cache
def otpverify(request):
    user=Users.objects.get(phone=phone)
    if request.method == 'POST':
        otp = request.POST.get('otp')
        account_sid = config('account_sid')
        auth_token = config('auth_token')
        client = Client(account_sid, auth_token)
        if(len(str(otp))==6):
            verification_check = client.verify \
                                .services(config('services')) \
                                .verification_checks \
                                .create(to= number, code= str(otp))
        else:
            messages.error(request,"Enter a valid OTP!")
            return render(request, 'otpverify.html')
        if verification_check.status == 'approved':
            login(request,user)
            return redirect('UserHome')
        else:
            messages.error(request,"Invalid OTP")
            return redirect ("OtpLogin")
    return render(request,'otpverify.html')





@never_cache
def editprofile(request):
    user = request.user
    form=UserUpdateForm(instance=user)
    if request.method == "POST":
        print("////////////////////////////////////////////////////")
        print(form)
        form=UserUpdateForm(request.POST,instance=user)
        if form.is_valid(): 
            SaveForm=form.save(commit=False)
            SaveForm.user=user
            SaveForm.save()
            messages.success(request,"Your account has been updated successfully!")
            return redirect('editprofile')
        else:
            messages.error(request,"Form isn't valid")
            print(form.errors)
    return render(request,"editprofile.html",{'form':form})


@never_cache
def userlogout(request):
    logout(request)
    return redirect("UserHome")

@never_cache
def userhome(request):
    return render(request, "userindex.html")






@never_cache
def usershop(request):
    products = Product.objects.all()
    catogeries = Catogery.objects.all().annotate(numpro=Count('product'))
    brands=Brand.objects.all().annotate(bpro=Count('product'))
    ptypes=PriceType.objects.all().annotate(ppro=Count('product'))
    context = {'products':products,'catogeries':catogeries,'brands':brands,'ptypes':ptypes}
    return render(request, "shop.html",context)

@never_cache
def filterview(request,id):
    catogery=Catogery.objects.all()
    catogeries = Catogery.objects.all().annotate(numpro=Count('product'))
    brand=Brand.objects.all()
    brands=Brand.objects.all().annotate(bpro=Count('product'))
    ptype=PriceType.objects.all()
    ptypes=PriceType.objects.all().annotate(ppro=Count('product'))
    products = Product.objects.filter(catogery=id)
    context = {'products':products,'catogeries':catogeries,'brands':brands,'ptypes':ptypes}
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

@never_cache
def filter_data(request):
    return Jsonresponse({'data':'hello'})


@never_cache
def usercart(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            order = Order.objects.get(customer=user,complete=False)
            items = order.orderitem_set.all()
        except:
            order=  []
            items = []
            page="Empty"
            return render(request,"cart.html",{'page':page})
        
        
        if(order==None or items==None):
            page="Empty"
            return render(request,"cart.html",{'page':page})
        else:
            context = {'items':items,'order':order}
            return render (request, "cart.html",context)
    else:
        items = []
        order=  []
    context = {'items':items,'order':order}
    return render (request, "cart.html",context)

@never_cache
def usercheckout(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            order = Order.objects.get(customer=user,complete=False)
            items = order.orderitem_set.all()
        except:
            order=  []
            items = []
            page="Empty"
            return render(request,"cart.html",{'page':page})
    form= MyAddressForm()
    addr = Address.objects.filter(cust=user)
    context = {'order':order,'items':items,'addr':addr,'form':form}
    return render(request, 'checkout.html', context )

@never_cache
def remove(request):
    user = request.user
    productId=request.GET.get("productid")
    print(productId)
    order = Order.objects.get(customer=user,complete=False)
    print(order)
    product = Product.objects.get(id=productId)
    print(product)
    order_item = OrderItem.objects.get(product=product, order=order)
    print(order_item)
    order_item.delete()
    response={'id':productId}
    return JsonResponse(response)
    return redirect('UserCart')
 
def userprofile(request):
    return render (request, "profile.html")

def profiledash(request):
    return render (request, "profiledash.html")

# def addaddress(request):
#     form= MyAddressForm()
#     if request.method == 'POST':
#         form = MyAddressForm(request.POST)
#         if form.is_valid():
#             address = form.save(commit=False)
#             address.cust=request.user
#             address.save()
#             return redirect("UserAddress")
#         else:
#             messages.error(request,"Error")
            
#     context={'form':form}
#     return render(request, "address.html",context)
    # return render (request, "address.html",context)

def profileorder(request):
    user = request.user
    orders =Order.objects.filter(customer=user,complete=True)
    items=OrderItem.objects.all()
    context={'orders':orders,'items':items}
    return render (request, "profileorders.html",context)


def wishlist(request):
    return render (request, "wishlist.html")



####################################   A D D R E S S  ##############################################################

def address(request):
    addr=Address.objects.filter(cust=request.user)
    user=request.user
    form= MyAddressForm()
    if request.method == 'POST':
        form = MyAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.cust=request.user
            address.save()
            return redirect("UserAddress")
        else:
            messages.error(request,"Error")
    context={'form':form,'addr':addr,'user':user}
    return render (request, "address.html",context)

def editaddress(request,pk):
    address = Address.objects.get(id=pk)
    form = MyAddressForm(instance=address)
    if request.method == 'POST':
        
        form = MyAddressForm(request.POST,instance=address)
        if form.is_valid():
            form.save()
            messages.success(request,'Updated Successfully')
            return redirect('UserAddress')
    return render(request,'editaddress.html',{'form':form,'id':pk})

def deleteaddress(request,pk):
    address = Address.objects.get(id=pk)
    address.delete()
    return redirect("UserAddress")


################################################################################################

# def addaddress(request):
#     form= MyAddressForm()
#     if request.method == 'POST':
#         form = MyAddressForm(request.POST)
#         if form.is_valid():
#             address = form.save(commit=False)
#             address.cust=request.user
#             address.save()
#             return redirect("UserAddress")
#         else:
#             messages.error(request,"Error")
            
#     context={'form':form}
#     return render(request, "address.html",context)
    # return render (request, "address.html",context)

def product(request,pk):
    product = Product.objects.get(id=pk)
    context = {'product':product}
    return render(request, "product.html",context)





def updateitem(request):
    customer = request.user
    customer = Users.objects.get(username=customer)
    productId = request.POST.get('productId')
    print(productId)
    action = request.POST.get('action')
    product = Product.objects.get(id=productId)
    print(action)
    cur_stock = product.stocks
    order, created = Order.objects.get_or_create(customer = customer , status='New',complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if  cur_stock > orderItem.quantity :
        flag = 0
    else :
        flag = 1
    if action == 'add' and cur_stock > orderItem.quantity :
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove' and orderItem.quantity > 1:
        orderItem.quantity = (orderItem.quantity - 1)
        if  cur_stock > orderItem.quantity :
            flag = 0
        else :
            flag = 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    response = {
        'items':order.get_cart_items,
        'quantity':orderItem.quantity,
        'total':orderItem.get_total,
        'cart_total':order.get_cart_total,
        'productId':productId,
        'cur_stock':cur_stock,
        'flag':flag
        }
    return JsonResponse(response)
  

@never_cache
def proceed(request):
    if request.method == 'POST':
        address_id = request.POST.get('address')
        address = Address.objects.get(id=address_id)
        user = request.user
        order= Order.objects.get(customer=user,complete=False)
        items = order.orderitem_set.all()
        for item in items :
            ordered = item.quantity
            print(item.quantity)
            prestocks = item.product.stocks
            poststocks = prestocks - ordered
            productid = item.product.id
            Product.objects.filter(id = productid).update(stocks = poststocks)
        total_amount=order.get_cart_total
        print(total_amount)
        Order.objects.filter(customer=user,complete=False).update(complete=True, address=address)
        transaction_id = order.id
        Pay.objects.get_or_create(order = order,method = 'COD',amount = total_amount,status = 'Completed',transactionid=transaction_id)
        response = {'':''}
        return JsonResponse(response)
    return render(request, "userindex.html")

# def razorpay(request):
#     if request.method == 'GET':
#         address_id = request.GET.get('address')
#         user = request.user
#         address= Address.objects.get(id=address_id)
#         order= Order.objects.get(customer = user,complete=False)
#         items = order.orderitem_set.all()
#         print(items)
#         for item in items :
#             ordered = item.quantity
#             print(item.quantity)
#             prestocks = item.product.stocks
#             poststocks = prestocks - ordered
#             productid = item.product.id
#             Product.objects.filter(id = productid).update(stocks = poststocks)
#         total_amount = order.get_cart_total
#         order.complete=True
#         order.address=Address.objects.get(id=address_id)
#         Pay.objects.get_or_create(order = order,method = 'RazorPay',amount = total_amount,status = 'Completed')
#         order.status = 'Placed'
#         order.save()
#         response = {'name':user.username,'email':user.email,'total':total_amount,'phone':user.phone,'status': 'Your order has been Placed Successfully'}
#         print(response)
#         return JsonResponse(response)
#     return render(request, "shop.html")


def payrazor(request):
    if request.method == 'GET':
        user=request.user
        print("////////////////////")
        print(user)
        order = Order.objects.get(customer = user,complete=False)
        total_amount =  order.get_cart_total
    return JsonResponse({'name':user.username,'email':user.email,'total':total_amount,'phone':user.phone })

@ csrf_exempt
def razorpay(request):
    user=request.user
    print(user)
    if request.method == 'POST': 
        order= Order.objects.get(customer=user,complete=False)
        items = order.orderitem_set.all()
        for item in items :
            ordered = item.quantity
            print(item.quantity)
            prestocks = item.product.stocks
            poststocks = prestocks - ordered
            productid = item.product.id
            Product.objects.filter(id = productid).update(stocks = poststocks)
        total_amount = order.get_cart_total
        transaction_id = request.POST.get('order_id')
        Pay.objects.get_or_create(order = order,method = 'RazorPay',amount = total_amount,status = 'Completed',transactionid=transaction_id)
        order.status = 'Pending'
        order.complete=True
        order.save()
        return JsonResponse({'status': 'Your order has been Placed Successfully'})


def cancelorder(request, id):
    order = Order.objects.get(id = id)
    items = OrderItem.objects.filter(order = order)
    order.status = 'Cancelled'
    for item in items :
        ordereditems = item.quantity
        cur_stock = item.quantity
        newstock = cur_stock + ordereditems
        productid = item.product.id
        Product.objects.filter(id = productid).update(stocks = newstock)
    order.save()
    return redirect('UserOrders')


def returnorder(request, id):
    order = Order.objects.get(id = id)
    items = OrderItem.objects.filter(order = order)
    order.status = 'RequestedCancellation'
    order.save()
    return redirect('UserOrders')


