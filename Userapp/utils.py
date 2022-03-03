import json
from Userapp.models import *
from Adminapp.models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart ={}
    print('Cart : ', cart)
    items = []
    order = {'get_cart_total':0,'get_cart_items':0}
    # cartItems = order['get_cart_items']
    for i in cart:
        # cartItems += cart[i]['quantity']
        product = Product.objects.get(id=i)
        total = (product.price * cart[i]["quantity"])
        order['get_cart_total'] += total
        order['get_cart_items'] += cart[i]['quantity']

        item = {
            'product' : product,
            'quantity':cart[i]['quantity'],
            'get_total':total
            }
        items.append(item)
        
    return {'order':order,'items':items} 