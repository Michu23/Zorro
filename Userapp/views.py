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
from django.db.models import Count,Sum
from django.http import JsonResponse
from decouple import config
from django.views.decorators.csrf import csrf_exempt
from babel.numbers import format_currency
from django.contrib.auth.decorators import login_required 
from django.db.models import Q
from django.template.loader import render_to_string
from django.core.paginator import EmptyPage , PageNotAnInteger , Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail


# Create your views here.

@never_cache
def userlogin(request):
    if request.user.is_authenticated:
        return redirect('UserHome')
    if request.method == "POST":
        uname = request.POST.get('username')
        password= request.POST.get('password')
        print(uname)
        try:
            user = Users.objects.get(username=uname)
            print("//////////same fields")
            
        except:
            messages.error(request,'User does not exists')
    
        try:
            user= authenticate(request,username=uname,password=password)
            print("//////////same fields")
            
            
            if user.adminstatus == False:
                print("//////////not blocked")
                login(request,user)
                return redirect ("UserHome")   
            else:
                messages.error(request,"You have been banned by the admin. Please call our customer care for more details!")
        except:
            messages.error(request,'Invalid Password')
            
    return render(request, "login.html")



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
def wishlist(request):
    print("//////////////////////////////////////")
    if request.user.is_authenticated:
        customer = request.user
    else :
        device = request.COOKIES['device']
        customer, created = CustomUser.objects.get_or_create(device=device)
    productId = request.GET.get('productId')
    print(productId)
    action = request.GET.get('action')
    print(action)
    product = Product.objects.get(id=productId)

    if action == 'add'  :
       wishes, created= Wishlist.objects.get_or_create(useradded = customer, productadded=product)
    else :
        wishes = Wishlist.objects.get(useradded = customer, productadded=product)
        wishes.delete()


    response = {'items':'flag'}
    return JsonResponse(response)
    

def mywish(request):
    user=request.user
    product=Product.objects.all()
    wishes= Wishlist.objects.filter(useradded = user).values_list('productadded',flat=True)

    wishlist= Wishlist.objects.filter(useradded = user)
    return render (request, 'wishlist.html',{"wishlist": wishlist,'wishes':wishes})

def removewish(request,id):
    user=request.user
    product=Product.objects.get(id=id)
    print(product.name)
    wishes= Wishlist.objects.filter(useradded =user,productadded=product)
    wishes.delete()
    return redirect("mywish")




####################################### SIGNUP ###################################################

@never_cache
def userreg(request):
    global regform,uname
    Users.objects.filter(is_active=False).delete()
    
    device = request.COOKIES['device']
    customer, created = Users.objects.get_or_create(device=device)
    
    form= MyUserFormUser()
    if request.method == 'POST':
        form = MyUserFormUser(request.POST,instance=customer)
        uname=request.POST.get("username")
        print(uname)
        umail=request.POST.get("email")
        uphone=request.POST.get("phone")
        request.session['phone'] = uphone
        un="Not taken"
        um="Not taken"
        up="Not taken"
        
        try:
            un = Users.objects.get(username=uname)
            print(un)
            messages.error(request,"Username already taken")
        except:
            pass
            
        try:
            um = Users.objects.get(email=umail)
            messages.error(request,"Email already taken")
        except:
            pass
        
        try:
            up = Users.objects.get(phone=uphone)
            messages.error(request,"Phone number already taken")
        except:
            pass
        
        if un == "Not taken":
            if(len(str(uphone))<=10):
                if form.is_valid():
                    regform=form.save(commit=False)
                    regform.is_active=False
                    regform.save()
                    return redirect ("SignupOtp")
                else:
                    messages.error(request,"Enter the details properly!")
            else:
                messages.error(request,"Enter a 10 digit-number!")
        else:
            messages.error(request,"Username , email or phone already taken")
                
    context={'form':form}
    return render(request, "reg.html",context)

@never_cache
def signupotp(request):
    phone = request.session.get('phone')
    if request.method == 'POST':
        number = '+91' + str(phone)
        request.session['phone'] = number
        account_sid = config('account_sid')
        auth_token = config('auth_token')
        client = Client(account_sid, auth_token)
        verification = client.verify \
                            .services(config('services')) \
                            .verifications \
                            .create(to=number, channel='sms')
        return redirect ('SignupOtpVerify')
    return render(request,'otploginsign.html',{'phone':phone})


@never_cache
def signupotpverify(request):
    number = request.session.get('phone')
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
            return render(request, 'otpverifysign.html')
        if verification_check.status == 'approved':
            regform.is_active=True
            regform.save()
            num=number[3:]
            print(num)
            user=Users.objects.get(phone=num)
            guest= Users.objects.get(username=uname)
            guest.device=""
            guest.save()
            try:
                del request.session['phone']
            except:
                pass
            login(request,user)
            return redirect('UserHome')
        else:
            messages.error(request,"Invalid OTP")
            return redirect ("SignupOtp")
    return render(request,'otpverifysign.html')


@never_cache
def userlogout(request):
    logout(request)
    return redirect("UserHome")


    if request.user.is_authenticated:
        customer=request.user
    else:
        try:
            device=request.COOKIES['device']
            customer,created=Users.objects.get_or_create(device=device)
            order,created= Order.objects.get_or_create(customer=customer,complete=False)
        except:
            return redirect("UserLogin")
        
    catogeries = Catogery.objects.all().annotate(numpro=Count('product'))
    brands=Brand.objects.all().annotate(bpro=Count('product'))
    ptypes=PriceType.objects.all().annotate(ppro=Count('product'))
    context = {'products':products,'catogeries':catogeries,'brands':brands,'ptypes':ptypes,'wishes':wishes}

@never_cache
def userhome(request):
    
    if request.user.is_authenticated:
        customer=request.user
        order,created= Order.objects.get_or_create(customer=customer,complete=False,status="New")

    else:
        try:
            device=request.COOKIES['device']
            print("////////////////////////////",device)
            customer,created=Users.objects.get_or_create(device=device,username=device)
            order,created= Order.objects.get_or_create(customer=customer,complete=False)
        except:
            return redirect("UserLogin")
    
    products = Product.objects.all()
    newproducts=Product.objects.all().order_by('-created')[:6]
    bestproducts=Product.objects.all().order_by('-price')[:6]


    wishes= Wishlist.objects.filter(useradded = customer).values_list('productadded',flat=True)
    context = {'products':products,'wishes':wishes,'newproducts':newproducts,'bestproducts':bestproducts}
    return render(request, "userindex.html",context)


@never_cache
def search(request):
    user=request.user
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-price').filter( Q(description__icontains=keyword) | Q(name__icontains=keyword) | Q(catogery__name__icontains=keyword) | Q(btype__bname__icontains=keyword) | Q(ptype__genre__icontains=keyword) | Q(price__icontains=keyword)  )
            productcount = products.count()

        else:
            messages.error(request,"No results found")
            return redirect("UserShop")
    
    catogeries = Catogery.objects.all().annotate(numpro=Count('product'))
    brands=Brand.objects.all().annotate(bpro=Count('product'))
    ptypes=PriceType.objects.all().annotate(ppro=Count('product'))

    wishes= Wishlist.objects.filter(useradded = user).values_list('productadded',flat=True)
    context = {'catogeries':catogeries,'brands':brands,'ptypes':ptypes,'products':products,'productcount':productcount,'wishes':wishes}


    return render (request,'shop.html',context)


@never_cache
def mail(request):
    if request.method == "POST":
        message=request.POST["mail"]
        send_mail('Zorro Estore Subscribed!',message,settings.EMAIL_HOST_USER,['m4michu123@gmail.com'],fail_silently=False)
        messages.success(request,"Submitted successfully!")
        return redirect('UserHome')

@never_cache
def contacts(request):
    if request.method == "POST":
        message=request.POST["message"]
        name=request.POST["name"]
        email=request.POST["email"]

        # send_mail('Zorro Estore Response',message,email,['m4michu123@gmail.com'],fail_silently=False)
        if name and message and email:
            try:
                send_mail(name, message, email, ['m4michu123@gmail.com'])
            except BadHeaderError:
                messages.error(request,'Invalid header found')
                return redirect('contacts')
            messages.success(request,"Form submitted successfully")
            return redirect('contacts')
        else:
        # In reality we'd use a form class
        # to get proper validation errors.
            messages.error("Make sure all fields are entered and valid.")
            return redirect('contacts')

    return render (request,"contact.html")

@never_cache
def usershop(request):
    if request.user.is_authenticated:
        customer=request.user
    else:
        try:
            device=request.COOKIES['device']
            customer,created=Users.objects.get_or_create(device=device)
        except:
            return redirect("UserLogin")
        
    products = Product.objects.all()
    paginator = Paginator (products, 9)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    productcount=products.count()

    wishes= Wishlist.objects.filter(useradded = customer).values_list('productadded',flat=True)
    catogeries = Catogery.objects.all().annotate(numpro=Count('product'))
    brands=Brand.objects.all().annotate(bpro=Count('product'))
    ptypes=PriceType.objects.all().annotate(ppro=Count('product'))
    context = {'products':paged_products,'catogeries':catogeries,'brands':brands,'ptypes':ptypes,'wishes':wishes,'count':productcount}
    return render(request, "shop.html",context)



@never_cache
def lowtohigh(request):
    if request.user.is_authenticated:
        customer=request.user
    else:
        try:
            device=request.COOKIES['device']
            customer,created=Users.objects.get_or_create(device=device)
            order,created= Order.objects.get_or_create(customer=customer,complete=False)
        except:
            return redirect("UserLogin")
        
    products = Product.objects.all().order_by('price')
    paginator = Paginator (products, 9)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    productcount=products.count()
    wishes= Wishlist.objects.filter(useradded = customer).values_list('productadded',flat=True)
    catogeries = Catogery.objects.all().annotate(numpro=Count('product'))
    brands=Brand.objects.all().annotate(bpro=Count('product'))
    ptypes=PriceType.objects.all().annotate(ppro=Count('product'))
    context = {'products':paged_products,'catogeries':catogeries,'brands':brands,'ptypes':ptypes,'wishes':wishes,'count':productcount}
    return render(request, "shop.html",context)

@never_cache
def hightolow(request):
    if request.user.is_authenticated:
        customer=request.user
    else:
        try:
            device=request.COOKIES['device']
            customer,created=Users.objects.get_or_create(device=device)
            order,created= Order.objects.get_or_create(customer=customer,complete=False)
        except:
            return redirect("UserLogin")
        
    products = Product.objects.all().order_by('-price')
    paginator = Paginator (products, 9)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    productcount=products.count()
    wishes= Wishlist.objects.filter(useradded = customer).values_list('productadded',flat=True)
    catogeries = Catogery.objects.all().annotate(numpro=Count('product'))
    brands=Brand.objects.all().annotate(bpro=Count('product'))
    ptypes=PriceType.objects.all().annotate(ppro=Count('product'))
    context = {'products':paged_products,'catogeries':catogeries,'brands':brands,'ptypes':ptypes,'wishes':wishes,'count':productcount}
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
    wishes= Wishlist.objects.filter(useradded = request.user).values_list('productadded',flat=True)

    context = {'products':products,'catogeries':catogeries,'brands':brands,'ptypes':ptypes,'wishes':wishes}
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
    wishes= Wishlist.objects.filter(useradded = request.user).values_list('productadded',flat=True)

    context = {'products':products,'catogeries':catogeries,'brands':brands,'ptypes':ptypes,'wishes':wishes}
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
    wishes= Wishlist.objects.filter(useradded = request.user).values_list('productadded',flat=True)

    context = {'products':products,'catogeries':catogeries,'brands':brands,'ptypes':ptypes,'wishes':wishes}
    return render(request, "shop.html",context)


@never_cache
def filter_shop_products(request):
    print("///////////////////")
    print(request.GET)
    if request.user.is_authenticated:
        customer = request.user     
    else :
        try:
            device = request.COOKIES['device']
            customer, created = CustomUser.objects.get_or_create(device=device)
        except :
            return redirect("UserLogin")    
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
    

    wishes = Wishlist.objects.filter(useradded = customer)
    print(wishes)
    t=render_to_string('filter.html',{'products':allProducts,'wishes':wishes})  
    return JsonResponse({'data': t})

@never_cache
def filter_data(request):
    return Jsonresponse({'data':'hello'})


def product(request,pk):
    product = Product.objects.get(id=pk)
    context = {'product':product}
    return render(request, "product.html",context)


def updateitem(request):
    if request.user.is_authenticated:
        customer= request.user
    else:
        device=request.COOKIES['device']
        print("////////////////////////////",device)
        customer= Users.objects.get(device=device)
    
    productId = request.POST.get('productId')
    print(productId)
    action = request.POST.get('action')
    product = Product.objects.get(id=productId)
    print("/////////////////////////////////////////////////////")
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
        'cart_total':order.get_cart_totall,
        'productId':productId,
        'cur_stock':cur_stock,
        'flag':flag
        }
    return JsonResponse(response)


  
@never_cache
def usercart(request):
    if request.user.is_authenticated:
        customer= request.user
        print("//////////////////////")
    else:
        device=request.COOKIES['device']
        print("////////////////////////////",device)
        customer= Users.objects.get(device=device)


    Order.objects.filter(customer=customer,complete=False,status="BuyNow").delete()

    try:
        order = Order.objects.get(customer=customer,complete=False,status="New")
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
    
    context = {'items':items,'order':order}
    return render (request, "cart.html",context)



@login_required(login_url="UserLogin")
def buynow(request,id):
    page="BuyNow"
    customer= request.user
    product = Product.objects.get(id=id)

    try:
        cur= Order.objects.filter(customer=customer,status="BuyNow",complete=False).order_by('-id')[0]
        cur.delete()
    except:
        pass
    
    order, created = Order.objects.get_or_create(customer = customer , status='BuyNow',complete=False)
    items, created = OrderItem.objects.get_or_create(order=order, product=product,quantity=1)


    try:
        coup = CouponUsed.objects.get(user=customer,used=True,applied=False)
        coup.delete()
        order.coupon_used=False
        order.save()
    except:
        pass
    
    form= MyAddressForm()
    addr = Address.objects.filter(cust=customer)
    context = {'product':product,'order':order,'items':items,'addr':addr,'form':form,'page':page}
    return render(request, 'checkout.html',context)



@never_cache
def remove(request):
    user = request.user
    productId=request.GET.get("productid")
    order = Order.objects.get(customer=user,complete=False,status="New")
    product = Product.objects.get(id=productId)
    order_item = OrderItem.objects.get(product=product, order=order)
    order_item.delete()
    response={'id':productId}
    return JsonResponse(response)
    return redirect('UserCart')


def userprofile(request):
    return render (request, "profile.html")

def profiledash(request):
    customers = Users.objects.all().count()
    orders = Order.objects.filter(customer=request.user).count()
    product_count = Product.objects.all().count()
    expense= Pay.objects.filter(payuser=request.user).aggregate(Sum("amount"))
    context= {'orders':orders,}
    return render (request, "profiledash.html")

@never_cache
def editprofile(request):
    user = request.user
    form=UserUpdateForm(instance=user)
    if request.method == "POST":
        print("////////////////////////////////////////////////////")
        print(form)
        form=UserUpdateForm(request.POST,request.FILES,instance=user)
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
    return redirect('UserOrders')


def returnorder(request, id):
    order = Order.objects.get(id = id)
    items = OrderItem.objects.filter(order = order)
    order.status = 'RequestedReturn'
    order.save()
    return redirect('UserOrders')

def profileorder(request):
    user = request.user
    orders =Order.objects.filter(customer=user,complete=True)
    items=OrderItem.objects.all()
    context={'orders':orders,'items':items}
    return render (request, "profileorder.html",context)

def profileorderdetails(request,id):
    user = request.user
    order = Order.objects.get(id=id)
    items=order.orderitem_set.all()
    context={'order':order,'items':items}
    return render (request, "profileorderdetails.html",context)


########################################################   A D D R E S S  ##############################################################

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




@never_cache
def proceed(request):
    if request.method == 'POST':
        address_id = request.POST.get('address')
        address = Address.objects.get(id=address_id)
        user = request.user

        try:
            order= Order.objects.get(customer=user,complete=False,status="BuyNow")
        except:
            order= Order.objects.get(customer=user,complete=False,status="New")

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
        try:
            if order.couponused.used==True:
                coupon_check = CouponUsed.objects.get(user = user,used = True,order = order)
                coupid=coupon_check.coupon
                coupon = CouponDetail.objects.get(id=coupid.id)
                print("old total........................",order.get_cart_oldtotal)
                lessed_money = (order.get_cart_oldtotal * coupon_check.coupon.percentage / 100)
                coupon.count = coupon.count + 1
                coupon.loss = coupon.loss +lessed_money
                coupon_check.loss=lessed_money
                coupon_check.applied=True
                order.coupon_used=True
                coupon.save()
                coupon_check.save()
                order.save()
            else:
                print("couponused isnt true!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        except:
            print("Error")


        
        # Order.objects.filter(customer=user,complete=False,status='New').update(complete=True, address=address,status = 'Placed')

        order.complete=True
        order.address= address
        order.status= 'Placed'
        order.save()


        transaction_id = order.id
        Pay.objects.get_or_create(payuser=user,order = order,method = 'COD',amount = total_amount,status = 'Completed',transactionid=transaction_id)
        response = {'':''}
        return JsonResponse(response)
    return render(request, "userindex.html")


def payrazor(request):
    if request.method == 'GET':
        user=request.user
        print("////////////////////")
        print(user)
        try:
            order= Order.objects.get(customer=user,complete=False,status="BuyNow")
        except:
            order= Order.objects.get(customer=user,complete=False,status="New")
        total_amount =  order.get_cart_total
    return JsonResponse({'name':user.username,'email':user.email,'total':total_amount,'phone':user.phone })


@csrf_exempt
def paypal(request):
    print("/////////////////////////////////activating paypal")
    if request.method == 'POST':        
        print("/////////////////////////////////activating paypal")

        user = request.user
        try:
            order= Order.objects.get(customer=user,complete=False,status="BuyNow")
        except:
            order= Order.objects.get(customer=user,complete=False,status="New")
        items = order.orderitem_set.all()
        for item in items :
            ordered = item.quantity
            prestocks = item.product.stocks
            poststocks = prestocks - ordered
            productid = item.product.id
            Product.objects.filter(id = productid).update(stocks = poststocks)
        total_amount = order.get_cart_total
        transactionid = order.id
        Pay.objects.get_or_create(payuser=user,order = order,method = 'Paypal',amount = total_amount,status = 'Completed', transactionid = transactionid)
        order.status = 'Placed'
        order.complete=True
        order.save()
        
        try:
            if order.couponused.used==True:
                coupon_check = CouponUsed.objects.get(user = user,used = True,order = order)
                coupid=coupon_check.coupon
                coupon = CouponDetail.objects.get(id=coupid.id)
                print("old total........................",order.get_cart_oldtotal)
                lessed_money = (order.get_cart_oldtotal * coupon_check.coupon.percentage / 100)
                coupon.count = coupon.count + 1
                coupon.loss = coupon.loss +lessed_money
                coupon_check.loss=lessed_money
                coupon_check.applied=True
                order.coupon_used=True
                coupon.save()
                coupon_check.save()
                order.save()
            else:
                print("couponused isnt true!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        except:
            print("Error")
        return JsonResponse({'status': 'Your order has been Placed Successfully'})
    
    
@never_cache
def verifycoupon(request):
    customer = request.user
    input_code = request.GET.get('input_code')


    last = Order.objects.filter(customer = customer,complete=False).order_by('-id')[0]
    if last.status == 'BuyNow' :
        order = Order.objects.get(customer = customer,status = 'BuyNow')
        items = OrderItem.objects.get(order = order)
    else :
        order= Order.objects.get(customer = customer,status = 'New')  
        items = order.orderitem_set.all()

    try:
        coup = CouponUsed.objects.get(user=customer,used=True,applied=False)
        coup.delete()
        print('/////////////////////')
        print(order.coupon_used)
        order.coupon_used=False
        order.save()
    except:
        pass

    try :
        coupon = CouponDetail.objects.get(code=input_code)
    except :
        data = {'total_amount' : order.get_cart_totall,'percentage':None,}
        return JsonResponse(data)

    
    lessed_money = (order.get_cart_total * coupon.percentage / 100)
    old_price = order.get_cart_total
    
    try:
        coupon_check = CouponUsed.objects.get(user = customer,coupon = coupon,used = True,applied = True)
        data = {'total_amount' : order.get_cart_totall,'percentage':'used',}
        return JsonResponse(data)
    except:
        apply_coupon = CouponUsed.objects.create(user = customer,coupon = coupon, used = True)
        print("////////////////new coupon used created")

    apply_coupon.used = True
    apply_coupon.order = order
    apply_coupon.loss = int(lessed_money)
    order.coupon_used = True
    CouponUsed.objects.get(user=customer,coupon=coupon).save()
    
    lessedinr = format_currency(lessed_money, 'INR', locale='en_IN')
    apply_coupon.save()
    print(order.get_cart_total)
    print(order.status)
    coupon.save()
    order.save()
    data = {'total_amount' : order.get_cart_totall,'percentage':coupon.percentage,'old_price':old_price ,'lessedmoney' :lessedinr}
    return JsonResponse(data)



@login_required(login_url="UserLogin")
@never_cache
def usercheckout(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            last = Order.objects.filter(customer = user,complete=False).order_by('-id')[0]
            if last.status == "BuyNow":
                last.delete()
            else:
                order = Order.objects.get(customer=user,complete=False,status="New")
                items = order.orderitem_set.all()
            
            
        except:
            order=  []
            items = []
            page="Empty"
            return render(request,"cart.html",{'page':page})

        try:
            coup = CouponUsed.objects.get(user=user,used=True,applied=False)
            coup.delete()
            order.coupon_used=False
            order.save()
        except:
            pass

    
    couponu = [i.coupon.code for i in CouponUsed.objects.all()]
    coup = CouponDetail.objects.exclude(code__in=couponu)
    
    form= MyAddressForm()
    addr = Address.objects.filter(cust=user)
    context = {'order':order,'items':items,'addr':addr,'form':form,'coupon':coup,'couponu':couponu}
    return render(request, 'checkout.html', context )

@ csrf_exempt
def razorpay(request):
    user=request.user
    print(user)
    if request.method == 'POST': 
        try:
            order= Order.objects.get(customer=user,complete=False,status="BuyNow")
            print("/////////////////////////////////buynow")
        except:
            print("/////////////////////////////////cart")
            order= Order.objects.get(customer=user,complete=False,status="New")
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
        Pay.objects.get_or_create(payuser=user,order = order,method = 'RazorPay',amount = total_amount,status = 'Completed',transactionid=transaction_id)
        order.status = 'Placed'
        order.complete=True
        
        order.save()

        
        try:
            if order.couponused.used==True:
                coupon_check = CouponUsed.objects.get(user = user,used = True,order = order)
                coupid=coupon_check.coupon
                coupon = CouponDetail.objects.get(id=coupid.id)
                print("old total........................",order.get_cart_oldtotal)
                lessed_money = (order.get_cart_oldtotal * coupon_check.coupon.percentage / 100)
                coupon.count = coupon.count + 1
                coupon.loss = coupon.loss +lessed_money
                coupon_check.loss=lessed_money
                coupon_check.applied=True
                order.coupon_used=True
                coupon.save()
                coupon_check.save()
                order.save()
            else:
                print("couponused isnt true!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        except:
            print("Error")


        return JsonResponse({'status': 'Your order has been Placed Successfully'})
    


def invoicedetails(request):
    user = request.user
    order = Order.objects.filter(customer = user,complete=True).order_by('-id')[0]
    items=order.orderitem_set.all()
    context={'order':order,'items':items}
    return render(request,'invoiceinfo.html',context)

