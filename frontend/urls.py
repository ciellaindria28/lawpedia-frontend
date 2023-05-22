from django.urls import path
from .views import *

app_name = "frontend"

urlpatterns = [
    path('', product_lists, name='home'),
    path('register', register_view, name='register'),
    path('login', login_view, name='login'),
    path('logout', logout, name='logout'),
    path('products/create', add_product, name='addproduct'),
    path('products', product_lists, name='product_lists'),
    path('cart/all', cart_view, name='cart'),
    path('add_to_cart', add_to_cart, name='add_to_cart'),
    path('cart/all', cart_view, name='cart_view'),
    path('download/orders', download_orders, name='download_orders'),
    path('generate/pdf', generate_pdf, name='generate_pdf'),
    path('update_quantity', update_quantity, name='update_quantity'),
    path('checkout',checkout, name ='checkout' )
]