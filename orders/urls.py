from django.urls import path
from .views import *

app_name = "orders"

urlpatterns = [
    path('', get_all_orders, name='orders'),
]