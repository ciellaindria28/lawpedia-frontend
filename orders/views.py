from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Orders
from .serializers import OrdersSerializer

@api_view(['GET'])
def get_all_orders(request):
    orders = Orders.objects.all()
    return Response(data=OrdersSerializer(orders, many = True).data, status= status.HTTP_200_OK)

