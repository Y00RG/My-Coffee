from django.urls import path
from . import views

urlpatterns = [
  path('add_to_cart', views.add_to_cart, name='add_to_cart'),
  path('cart', views.cart, name='cart'),
  path('remove_from_cart/<int:order_details_id>', views.remove_from_cart, name='remove_from_cart'),
  path('increment_qty/<int:order_details_id>', views.increment_qty, name='increment_qty'),
  path('decrement_qty/<int:order_details_id>', views.decrement_qty, name='decrement_qty'),
  path('payment', views.payment, name='payment'),
  path('show_orders', views.show_orders, name='show_orders'),
  
]