from django.urls import path
from .views import *

app_name = "frontend"

urlpatterns = [
    path('register', register_view, name='register'),
    path('login', login_view, name='login'),
    path('logout', logout, name='logout'),
    path('products/create', add_product, name='addproduct'),
    path('products', product_list, name='product_list'),
    path('cart/all', cart_view, name='cart'),
    path('orders', order_list, name='order_list'),
    path('download/orders', download_orders, name='download_orders'),
    path('generate/pdf', generate_pdf, name='generate_pdf'),
    
]