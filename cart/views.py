from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

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