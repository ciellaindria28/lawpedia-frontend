from django.urls import path
from .views import *

app_name = "frontend"

urlpatterns = [
    path('login', login_view, name='login'),
    path('addproduct', add_product, name='addproduct'),
    path('product_list', product_list, name='product_list'),
    path('cart', cart_view, name='cart'),
    path('order_list', order_list, name='order_list'),

]