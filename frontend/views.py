from django.shortcuts import render

# Create your views here.

def login_view(request):
    return render(request, 'login.html')


def add_product(request):
    return render(request,'productform.html')

def product_list(request):
    return render(request, 'productlist.html')

def cart_view(request):
    return render(request, 'cart_view.html')

def order_list(request):
    return render(request, 'order_list.html')

def order_detail(request):
    return render(request, 'order_detail.html')
