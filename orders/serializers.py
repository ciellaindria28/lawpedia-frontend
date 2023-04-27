from rest_framework import serializers
from .models import Orders

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['id', 'username', 'total_price', 'status_order']
