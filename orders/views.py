from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Orders, ItemOrders
from .serializers import OrdersSerializer, ItemOrdersSerializer
from django.http import HttpRequest
import requests
import json

LAWPEDIA_AUTH = 'http://localhost:8001/auth/user'

@api_view(['GET'])
def get_all_orders(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    except:
        return Response(data={"error": "No token provided."}, status=status.HTTP_401_UNAUTHORIZED)
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(LAWPEDIA_AUTH, headers=headers)
    if response.status_code == 200:
        response_body = json.loads(response.text)
        username = response_body['data']['username']
        orders = Orders.objects.filter(seller_username=username)
        orders_serialized = []
        for order in orders:
            serialized_order = OrdersSerializer(order).data
            item_orders = ItemOrders.objects.filter(orders = order)
            serialized_item_orders = ItemOrdersSerializer(item_orders, many = True)
            serialized_order['products'] = serialized_item_orders.data
            orders_serialized.append(serialized_order)
        
        return Response(data=orders_serialized, status= status.HTTP_200_OK)
    else:
        return Response(data={"error": "Token not valid."}, status=status.HTTP_401_UNAUTHORIZED)
        

@api_view(['GET'])
def get_order_by_id(request, order_id):
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    except:
        return Response(data={"error": "No token provided."}, status=status.HTTP_401_UNAUTHORIZED)
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(LAWPEDIA_AUTH, headers=headers)
    if response.status_code == 200:
        response_body = json.loads(response.text)
        username = response_body['data']['username']
        try:
            order = Orders.objects.get(id=order_id)
            order_buyer_username = order.buyer_username
            order_seller_username = order.seller_username
            
            if username == order_buyer_username or username == order_seller_username:
                serialized_order = OrdersSerializer(order).data
                item_orders = ItemOrders.objects.filter(orders = order)
                serialized_item_orders = ItemOrdersSerializer(item_orders, many = True)
                serialized_order['products'] = serialized_item_orders.data
                return Response(data=serialized_order, status=status.HTTP_200_OK)
            else:
                return Response(data={"error": "This is not your order."}, status=status.HTTP_403_FORBIDDEN)
        except Orders.DoesNotExist:
            return Response(data={"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        
    else:
        return Response(data={"error": "Token not valid."}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
def update_order_status(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    except:
        return Response(data={"error": "No token provided."}, status=status.HTTP_401_UNAUTHORIZED)
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(LAWPEDIA_AUTH, headers=headers)
    if response.status_code == 200:
        response_body = json.loads(response.text)
        username = response_body['data']['username']
        
        if request.data.get('id') == None or request.data.get('newStatus') == None:
            return Response(data={"error": "There are missing parameters."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            order_id = request.data.get('id')
            order = Orders.objects.get(id=order_id)
            
            if order.seller_username != username:
                return Response(data={"error": "You don't have access to update this order."}, status=status.HTTP_403_FORBIDDEN)
            
            status_value = request.data.get('newStatus')
            order.status_order = status_value
            order.save()
            serialized_order = OrdersSerializer(order)
            return Response(data=serialized_order.data, status=status.HTTP_200_OK)
        except Orders.DoesNotExist:
            return Response(data={"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        
    else:
        return Response(data={"error": "Token not valid."}, status=status.HTTP_401_UNAUTHORIZED)
    
        
    

@api_view(['POST'])
def confirm_delivery(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    except:
        return Response(data={"error": "No token provided."}, status=status.HTTP_401_UNAUTHORIZED)
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(LAWPEDIA_AUTH, headers=headers)
    username = ''
    if response.status_code == 200:
        response_body = json.loads(response.text)
        username = response_body['data']['username']
    else:
         return Response(data={"error": "Token not valid."}, status=status.HTTP_401_UNAUTHORIZED)
    
    if request.data.get('id') == None:
        return Response(data={"error": "There are missing parameters."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        order_id = request.data.get('id')
        order = Orders.objects.get(id=order_id)
        
        if order.buyer_username != username:
            return Response(data={"error": "You don't have access to confirm this delivery."}, status=status.HTTP_403_FORBIDDEN)
            
        status_value = "delivered"
        order.status_order = status_value
        order.save()
        serialized_order = OrdersSerializer(order)
        return Response(data=serialized_order.data, status=status.HTTP_200_OK)
    except Orders.DoesNotExist:
        return Response(data={"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def checkout(request):
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
    
    if request.data.get('username') == None or request.data.get('cartProductsId') == None:
        return Response(data={"error": "There are missing parameters."}, status=status.HTTP_400_BAD_REQUEST)
    
    username = request.data['username']
    if token_username != username:
        return Response(data={"error": "You don't have access to checkout this order."}, status=status.HTTP_403_FORBIDDEN)
    
    item_ids = request.data.get('cartProductsId', [])  # Retrieve the list of item IDs from the request data
    cart_products = []

    # 1. Get all cart products
    for item_id in item_ids:
        sub_request = HttpRequest()
        sub_request.method = 'GET'
        sub_request.GET['item_id'] = item_id
        response = get_cart_products_by_id(sub_request, item_id)  # TODO: Replace with real method
        
        if response.status_code == status.HTTP_200_OK:
            cart_product = response.data
            cart_products.append(cart_product)

    

    # 2. Check seller stocks and create new item
    item_orders = []
    total_price = 0
    for item in cart_products:
        product_id = item['productId']
        sub_request = HttpRequest()
        sub_request.method = 'GET'
        sub_request.GET['item_id'] = product_id
        response = check_seller_product_stock_by_id(sub_request, product_id) # TODO: Replace with real method
        if response.status_code == status.HTTP_200_OK:
            product_from_seller = response.data
            if item['quantity'] <= product_from_seller['stok']:
                item_orders.append([item['quantity'], product_from_seller])
                total_price+= item['quantity'] * product_from_seller['price']
            
    
    
    # 3. Pay
    
    # Make the new Orders object
    order = Orders.objects.create(
        buyer_username=username,
        total_price=total_price,
        status_order='paid',
        seller_username=cart_products[0]['sellerUsername']
    )
    # Make the new itemOrders object based on item_orders
    
    for item in item_orders:
        new_item_order = ItemOrders.objects.create(
            product_id=item[1]['id'],
            product_name = item[1]['name'],
            orders=order,
            quantity=item[0],
            price=item[0] * item[1]['price']
        )
    
    pay_data = {'orderId': order.id}
    pay_request = HttpRequest()
    pay_request.method = 'POST'
    pay_request.data = pay_data
    response = pay(pay_request) # TODO: Replace with real method
    
    serialized_order = OrdersSerializer(order).data
    
    item_orders = ItemOrders.objects.filter(orders = order)
    serialized_item_orders = ItemOrdersSerializer(item_orders, many = True)
    serialized_order['products'] = serialized_item_orders.data
    
    
    return Response(data=serialized_order, status=status.HTTP_200_OK)



@api_view(['GET'])
def get_cart_products_by_id(request, item_id):
    #TODO: DUMMY, remove soon when ciella Done
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

@api_view(['GET'])
def check_seller_product_stock_by_id(request, item_id):
    #TODO: DUMMY, remove soon when Kevin Done
    if item_id == 1:
        data = {"id" : 1, 
                "username" : "trudy",
                "name": "Product A", 
                "price": 10000, 
                "stok": 5, 
                "description": "produk ini baru diupdate", 
                "category": "Electronics" 
                }  
    elif item_id == 2:
        data = {"id" : 2, 
                "username" : "trudy",
                "name": "Product B", 
                "price": 20000, 
                "stok": 5, 
                "description": "produk ini baru diupdate", 
                "category": "Electronics" 
                }   
    else :
        data = {"id" : 3, 
                "username" : "trudy",
                "name": "Product C", 
                "price": 30000, 
                "stok": 1, 
                "description": "produk ini baru diupdate", 
                "category": "Electronics" 
                }  
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['POST'])
def pay(request):
    #TODO: David
    order_id = request.data.get('orderId')
    return Response(status=status.HTTP_200_OK)
    