from django.urls import path
from .views import *

app_name = "frontend"

urlpatterns = [
    path('login', login_view, name='login'),
    path('products/create', add_product, name='addproduct'),
    path('products', product_list, name='product_list'),
    path('cart/all', cart_view, name='cart'),
    path('orders', order_list, name='order_list'),

]