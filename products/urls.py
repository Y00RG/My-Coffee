from django.urls import path
from . import views

urlpatterns = [
  path('', views.products, name='products'),
  path('<int:pro_id>', views.product, name='product'), # Reach product by it's id
  path('search', views.search, name='search'),
  
]

