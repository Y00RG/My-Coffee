from django.shortcuts import get_object_or_404, render
from .models import Product


def products(request):
  
  pro = Product.objects.all()
  name=None
  desc=None
  price_from=None
  price_to=None
  case_sensitive=None
  
  # Manage search
  if 'case_sensitive' in request.GET:
    case_sensitive=request.GET['case_sensitive']
    if not case_sensitive:
      case_sensitive = 'off'
  
  if 'search_name' in request.GET:
    name = request.GET['search_name']
    if name:
      if case_sensitive=='on':
        # name__contains cares about char case (sensitive)
        pro = pro.filter(name__contains=name)
      else:
        # name__icontains doesn't care about char case (insensitive)
        pro = pro.filter(name__icontains=name)


  if 'search_desc' in request.GET:
    desc = request.GET['search_desc']
    if desc:
      if case_sensitive=='on':
        pro = pro.filter(description__contains=desc)
      else:
        pro = pro.filter(description__icontains=desc)


  if 'search_price_from' in request.GET and 'search_price_to' in request.GET:
    price_from = request.GET['search_price_from']
    price_to = request.GET['search_price_to']
    if price_from and price_to:
      if price_from.isdigit() and price_to.isdigit():
        # price__gte => greater the or equal
        # price__lte => less than or equal
        pro = pro.filter(price__gte=price_from, price__lte=price_to)
  
  context = {
    'products':pro,

  }
  return render(request, 'products/products.html', context)


def product(request, pro_id): #render pro_id from urls and manage 404 page
  context = {
    'pro':get_object_or_404(Product, pk=pro_id)
  }
  return render(request, 'products/product.html', context)


def search(request):
  return render(request, 'products/search.html')

