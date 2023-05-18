from django.urls import path
from .views import *

app_name = "cart"

urlpatterns = [
    path('<int:item_id>', get_cart_products_by_id, name='get_cart_products_by_id'),
    path('add', add_product_to_cart, name='add_product_to_cart'),
]
