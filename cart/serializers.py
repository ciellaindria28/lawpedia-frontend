from rest_framework import serializers
from .models import Cart

class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('cartProductId', 'productId', 'productName','price','quantity', 'buyerUsername', 'sellerUsername')
