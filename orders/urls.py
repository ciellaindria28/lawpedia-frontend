from django.urls import path
from .views import *

app_name = "orders"

urlpatterns = [
    path('', get_all_orders, name='orders'),
    path('<int:order_id>', get_order_by_id, name='get_order_by_id'),
    path('updateStatus', update_order_status, name='update_order_status'),
    path('confirmDelivery', confirm_delivery, name='confirm_delivery'),
    path('checkout', checkout, name='checkout'),
    path('cart/<int:item_id>', get_cart_products_by_id, name='get_cart_products_by_id'),
    path('product/<int:item_id>', check_seller_product_stock_by_id, name='check_seller_product_stock_by_id'),
]