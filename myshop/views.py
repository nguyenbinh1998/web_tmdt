import json
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from myshop.models import Customer, Order, OrderItem, Product, ShippingAddress
from datetime import datetime


def store(request):
    if request.user.is_authenticated:
        customer = get_object_or_404(Customer, user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        order = {'get_cart_total': 0, 'get_cart_item':0, 'shipping':False}
    products = Product.objects.all()
    return render(request, 'myshop/store.html', {'products':products, 'order':order})

def cart(request):
    if request.user.is_authenticated:
        customer = get_object_or_404(Customer, user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item':0, 'shipping':False}
    return render(request, 'myshop/cart.html', {'items':items, 'order':order})

def checkout(request):
    if request.user.is_authenticated:
        customer = get_object_or_404(Customer, user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        order = {'get_cart_total': 0, 'get_cart_item':0, 'shipping':False}
        items = []
    return render(request, 'myshop/checkout.html', {'items':items, 'order':order})

def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity += 1
    elif action == "remove":
        orderItem.quantity -= 1
    orderItem.save()
    
    if orderItem.quantity == 0:
        orderItem.delete()

    return JsonResponse('It was sent', safe=False)

def processOrder(request):
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = data['userFormData']['total']
        if total == order.get_cart_total:
            order.complete = True
        order.save()
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                zipcode=data['shipping']['zipcode'],
                state=data['shipping']['state'],
            )
    return JsonResponse('Payment completed', safe=False)