from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product
from orders.models import Order
from orders.models import OrderDetails
from .models import Payment
from django.utils import timezone


def add_to_cart(request):
  
  if 'pro_id' in request.GET and 'qty' in request.GET and 'price' in request.GET and request.user.is_authenticated and not request.user.is_anonymous:
    
    pro_id = request.GET['pro_id']
    qty = request.GET['qty']
    order = Order.objects.all().filter(user=request.user, is_finished=False)
    
    if not Product.objects.all().filter(id=pro_id).exists():
      return redirect('products')
    
    pro = Product.objects.get(id=pro_id)
    
    if order:
      old_order = Order.objects.get(user=request.user, is_finished=False)
      
      if OrderDetails.objects.all().filter(order=old_order, product=pro).exists():
        order_details = OrderDetails.objects.get(order=old_order, product=pro)
        order_details.quantity += int(qty)
        order_details.save()
      else:
        order_details = OrderDetails.objects.create(
          product = pro,
          order = old_order,
          price = pro.price,
          quantity=qty
        )
      messages.success(request, 'Was added to cart for Old order')
      
    else:
      new_order = Order()
      new_order.user = request.user
      new_order.order_date = timezone.now()
      new_order.is_finished = False
      new_order.save()
      
      order_details = OrderDetails.objects.create(
        product = pro,
        order = new_order,
        price = pro.price,
        quantity=qty
      )
      
      messages.success(request, 'Was added to cart for New order')
    
    return redirect('/products/' + request.GET['pro_id'])
  else:  
    if 'pro_id' in request.GET:
      messages.error(request, 'You Must Be Logged In!')
      return redirect('/products/' + request.GET['pro_id'])
    else:
      return redirect('index')


def cart(request):
  context = None
  
  if request.user.is_authenticated and not request.user.is_anonymous:
    if Order.objects.all().filter(user=request.user, is_finished=False):
      order = Order.objects.get(user=request.user, is_finished=False)
      order_details = OrderDetails.objects.all().filter(order=order)
      total = 0
      
      for sub in order_details:
        total += sub.price * sub.quantity
      
      context = {
        'order':order,
        'order_details':order_details,
        'total':total,
      }
      
  return render(request, 'orders/cart.html', context)


def remove_from_cart(request, order_details_id):
  if request.user.is_authenticated and not request.user.is_anonymous and order_details_id:
    order_details = OrderDetails.objects.get(id=order_details_id)
    
    # make sure the current user is only allowed to delete an order
    if order_details.order.user.id == request.user.id:
      order_details.delete()
    
  return redirect('cart')


def increment_qty(request, order_details_id):
  if request.user.is_authenticated and not request.user.is_anonymous and order_details_id:
    order_details = OrderDetails.objects.get(id=order_details_id)
    
    if order_details.order.user.id == request.user.id:
      order_details.quantity += 1
      order_details.save()
    
  return redirect('cart')


def decrement_qty(request, order_details_id):
  if request.user.is_authenticated and not request.user.is_anonymous and order_details_id:
    order_details = OrderDetails.objects.get(id=order_details_id)
    
    if order_details.order.user.id == request.user.id:
      if order_details.quantity > 1:
        order_details.quantity -= 1
        order_details.save()
    
  return redirect('cart')


def payment(request):
  context = None
  shipment_address = None
  shipment_phone = None
  card_number = None
  expire = None
  security_code = None
  is_added = None
  
  if request.method == 'POST' and 'btn_payment' in request.POST and 'shipment_address' in request.POST and 'shipment_phone' in request.POST and 'card_number' in request.POST and 'expire' in request.POST and 'security_code' in request.POST:

    shipment_address = request.POST['shipment_address']
    shipment_phone = request.POST['shipment_phone']
    card_number = request.POST['card_number']
    expire = request.POST['expire']
    security_code = request.POST['security_code']
    
    if request.user.is_authenticated and not request.user.is_anonymous:
      if Order.objects.all().filter(user=request.user, is_finished=False):
        order = Order.objects.get(user=request.user, is_finished=False)
        payment = Payment(
          order=order,
          shipment_address=shipment_address,
          shipment_phone=shipment_phone,
          card_number=card_number,
          expire=expire,
          security_code=security_code)
        
        payment.save()
        order.is_finished=True
        order.save()
        is_added=True
        
        messages.success(request, 'Your Order Is Finished')
        
    context = {
      'shipment_address':shipment_address,
      'shipment_phone':shipment_phone,
      'card_number':card_number,
      'expire':expire,
      'security_code':security_code,
      'is_added':is_added,
    }
    
  else:
    if request.user.is_authenticated and not request.user.is_anonymous:
      if Order.objects.all().filter(user=request.user, is_finished=False):
        order = Order.objects.get(user=request.user, is_finished=False)
        order_details = OrderDetails.objects.all().filter(order=order)
        total = 0
        
        for sub in order_details:
          total += sub.price * sub.quantity
        
        context = {
          'order':order,
          'order_details':order_details,
          'total':total,
        }
  
  return render(request, 'orders/payment.html', context)


def show_orders(request):
  context = None
  all_orders = None
  
  if request.user.is_authenticated and not request.user.is_anonymous:
    all_orders =  Order.objects.all().filter(user=request.user)
    
    if all_orders:
      for x in all_orders:
        order = Order.objects.get(id=x.id)
        order_details = OrderDetails.objects.all().filter(order=order)
        total = 0
          
        for sub in order_details:
          total += sub.price * sub.quantity
          
        x.total = total
        x.items_count = order_details.count
      
  context = {
    'all_orders':all_orders
  }
  return render(request, 'orders/show_orders.html', context)
  