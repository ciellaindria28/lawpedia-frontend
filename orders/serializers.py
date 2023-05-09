from rest_framework import serializers
from .models import Orders, ItemOrders

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['id', 'buyer_username', 'total_price', 'status_order', 'seller_username']

class ItemOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOrders
        fields = ['product_name', 'quantity', 'price']
