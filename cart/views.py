from asyncio import DatagramTransport
from urllib.request import DataHandler
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from cart.models import Cart
from .serializers import CartProductSerializer
from django.http import HttpRequest
import requests
import json

# Create your views here.

LAWPEDIA_AUTH = 'http://localhost:8001/auth/user'
LAWPEDIA_PRODUCT = 'http://localhost:3000/products'

@api_view(['GET'])
def get_cart_products_by_id(request, item_id):
    #TODO: Return data with format like dummy
    if item_id == 1:
        data = {"cartProductId": 1, 
                "productId": 1, 
                "quantity": 3,  
                "buyerUsername": "alice", 
                "sellerUsername": "trudy", 
                } 
    elif item_id == 2:
        data = {"cartProductId": 2, 
                "productId": 2, 
                "quantity": 2,  
                "buyerUsername": "alice", 
                "sellerUsername": "trudy", 
                } 
    else :
        data = {"cartProductId": 3, 
                "productId": 3, 
                "quantity": 4,  
                "buyerUsername": "alice", 
                "sellerUsername": "trudy", 
                }
    return Response(data=data, status=status.HTTP_200_OK)


#Add product to cart
@api_view(['POST'])
def add_product_to_cart(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    except:
        return Response(data={"error": "No token provided."}, status=status.HTTP_401_UNAUTHORIZED)
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(LAWPEDIA_AUTH, headers=headers)
    token_username = ''

    if response.status_code == 200:
        response_body = json.loads(response.text)
        token_username = response_body['data']['username']
    else:
         return Response(data={"error": "Token not valid."}, status=status.HTTP_401_UNAUTHORIZED)
    
    productId = request.data['productId']
    quantity = request.data['quantity']

    # Check product stock using the external function
    sub_request = HttpRequest()
    sub_request.method = 'GET'
    response = check_seller_product_stock_by_id(sub_request, productId, token)
    data = response.data
    product_quantity = data['stock']

    #Check if stock satisfies the quantity 
    if product_quantity >= quantity:
        # Create a new CartProduct instance
        cart_product = Cart.objects.create(
        productId=productId,
        quantity=quantity,
        buyerUsername=token_username,
        sellerUsername=data['username']
        )
        
        # Prepare the JSON response
        cart_product_serialized = CartProductSerializer(cart_product).data
            
        # Return the JSON response
        return Response(data=cart_product_serialized, status=status.HTTP_200_OK)
    
    else:
        return Response(data={"error": "Insufficient product quantity."}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def check_seller_product_stock_by_id(request, item_id, token):
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{LAWPEDIA_PRODUCT}/{item_id}", headers=headers)
    
    data = json.loads(response.text)
    return Response(data=data, status=status.HTTP_200_OK)

