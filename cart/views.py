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

#Get cart based on id
@api_view(['GET'])
def get_cart_products_by_id(request,item_id):
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    except:
        return Response(data={"error": "No token provided."}, status=status.HTTP_401_UNAUTHORIZED)
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(LAWPEDIA_AUTH, headers=headers)
    if response.status_code == 200:
        try:
            cart = Cart.objects.get(cartProductId=item_id)
            serialized_cart = CartProductSerializer(cart).data
            return Response(data=serialized_cart, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response(data={"error": "Cart with the provided id does not exist."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(data={"error": "Token not valid."}, status=status.HTTP_401_UNAUTHORIZED)

#Get all carts
@api_view(['GET'])
def get_all_carts(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    except:
        return Response(data={"error": "No token provided."}, status=status.HTTP_401_UNAUTHORIZED)
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(LAWPEDIA_AUTH, headers=headers)
    if response.status_code == 200:
        response_body = json.loads(response.text)
        username = response_body['data']['username']
        carts = Cart.objects.filter(buyerUsername=username)
        carts_serialized = []
        for cart in carts:
            serialized_cart = CartProductSerializer(cart).data
            carts_serialized.append(serialized_cart)
        return Response(data=carts_serialized, status= status.HTTP_200_OK)
    else:
        return Response(data={"error": "Token not valid."}, status=status.HTTP_401_UNAUTHORIZED)


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


#function to check product stock
@api_view(['GET'])
def check_seller_product_stock_by_id(request, item_id, token):
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{LAWPEDIA_PRODUCT}/{item_id}", headers=headers)
    
    data = json.loads(response.text)
    return Response(data=data, status=status.HTTP_200_OK)

    
#Update quantity
@api_view(['PUT'])
def update_cart_quantity(request):
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
    
    cartId = request.data.get('cartId')
    quantity = request.data.get('quantity')

    try:
        cart = Cart.objects.get(cartProductId=cartId)
        productId = cart.productId
    except Cart.DoesNotExist:
        return Response(data={"error": "Cart with the provided cartId does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        # Check product stock using the external function
        sub_request = HttpRequest()
        sub_request.method = 'GET'
        response = check_seller_product_stock_by_id(sub_request, productId, token)
        data = response.data
        product_quantity = data['stock']

        # Check if stock satisfies the quantity 
        if product_quantity >= quantity:
            # Update the stock of the cart
            cart.quantity = quantity
            cart.save()
            
            # Prepare the JSON response
            cart_product_serialized = CartProductSerializer(cart).data
                
            # Return the JSON response
            return Response(data=cart_product_serialized, status=status.HTTP_200_OK)
        
        else:
            return Response(data={"error": "Insufficient product quantity."}, status=status.HTTP_400_BAD_REQUEST)
    
    except requests.exceptions.RequestException:
        return Response(data={"error": "Failed to connect to the external API."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#Delete cart
@api_view(['DELETE'])
def delete_cartproduct(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    except:
        return Response(data={"error": "No token provided."}, status=status.HTTP_401_UNAUTHORIZED)
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(LAWPEDIA_AUTH, headers=headers)
    if response.status_code == 200:
        cartId = request.data['cartId']
        try:
            cart = Cart.objects.get(cartProductId=cartId)
            cart.delete()
            return Response(data={"message": "Cart successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response(data={"error": "Cart with the provided id does not exist."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(data={"error": "Token not valid."}, status=status.HTTP_401_UNAUTHORIZED)
   



