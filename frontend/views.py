from re import L
from django.shortcuts import render, redirect
import requests
from .endpoints import *
import json
from django.http import HttpResponse,JsonResponse
from django.contrib import messages

# Create your views here.

def register_view(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = int(request.POST.get('role'))
        
        if password1 != password2:
            context = {'message': 'Passwords do not match'}
            return render(request, 'register.html', context)
        
        response = requests.post(REGISTER_URL, data={'username': username, 'email': email, 'password1': password1, 'password2': password2, 'role': role})
        if response.status_code == 201:
            return redirect('frontend:login')
        context = {'message': 'Something went wrong'}
        return render(request, 'register.html', context)

def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        response = requests.post(LOGIN_URL, data={'username': username, 'password': password})
        if response.status_code == 200:
            # save the token in the session
            response_data = json.loads(response.text)
            access_token = response_data["data"]["tokens"]["access"]
            refresh_token = response_data["data"]["tokens"]["refresh"]
            role = response_data["data"]["role"]
            username = response_data["data"]["username"]

            request.session['access_token'] = access_token
            request.session['refresh_token'] = refresh_token
            request.session['username'] = username
            request.session['role'] = role
            return redirect('frontend:product_lists')
        context = {'message': 'Invalid credentials'}
        return render(request, 'login.html', context)
    
def logout(request):
    try:
        access_token = request.session.get('access_token')
        response = requests.post(LOGOUT_URL, headers={'Authorization': 'Bearer ' + access_token})
        if response.status_code == 200:
            # remove the token from the session
            del request.session['access_token']
            del request.session['refresh_token']
            del request.session['username']
            return redirect('frontend:login')
        return redirect('frontend:login')
    except:
        return redirect('frontend:login')
    
def download_orders(request):
    # verify user
    try:
        response = requests.get(USER_CHECK_URL, headers={'Authorization': 'Bearer ' + request.session.get('access_token')})
        if response.status_code == 401:
            return redirect('frontend:login')
    except:
        return redirect('frontend:login')
    username = request.session.get('username')
    if username is None:
        return redirect('frontend:login')
    context = {'username': username}
    context['role'] = request.session.get('role')
    
    if context['role'] == 1:
        return redirect('frontend:product_lists')
    
    access_token = request.session.get('access_token')
    response = requests.get(GET_PDF_LIST, headers={'Authorization': 'Bearer ' + access_token})
    if response.status_code == 200:
        response_data = json.loads(response.text)
        pdf_list = response_data["data"]
        context['pdfs'] = pdf_list
    return render(request, 'download_orders.html', context)

def generate_pdf(request):
    access_token = request.session.get('access_token')
    response = requests.get(CREATE_PDF_URL, headers={'Authorization': 'Bearer ' + access_token})
    if response.status_code == 200:
        response_data = json.loads(response.text)
        message = response_data["data"]["message"]
        messages.success(request, message)
        return redirect ('frontend:download_orders')
    else:
        context = {'failed': 'Something went wrong'}
        return render(request, 'download_orders.html', context)
    
def add_product(request):
    if request.method == 'POST':
        try:
            response = requests.get(USER_CHECK_URL, headers={'Authorization': 'Bearer ' + request.session.get('access_token')})
            if response.status_code == 401:
                context = {'username': None}
            else:
                user_data = response.json()
                if user_data.get('role') == 2:  # Check if the user has role == 2 (seller)
                    username = request.session.get('username')
                    name = request.POST.get('name')
                    price = request.POST.get('price')
                    stock = request.POST.get('stock')
                    description = request.POST.get('description')
                    category = request.POST.get('category')

                    # Prepare the request data
                    data = {
                        'username': username,
                        'name': name,
                        'price': price,
                        'stock': stock,
                        'description': description,
                        'category': category
                    }

                    # Send the POST request to create a product
                    response = requests.post(CREATE_PRODUCT_URL, data=data)

                    # Check the response status code
                    if response.status_code == 201:
                        # Product created successfully
                        context = {'username': request.session.get('username')}
                    else:
                        # Error occurred while creating the product
                        context = {'username': None}
                else:
                    # User does not have the required role
                    context = {'username': None}
        except:
            context = {'username': None}
    else:
        context = {'username': request.session.get('username')}
    
    return render(request, 'productform.html', context)


def product_lists(request):
    context = {}
    try:
        response = requests.get(USER_CHECK_URL, headers={'Authorization': 'Bearer ' + request.session.get('access_token')})
        if response.status_code == 401:
            context = {'username': None}
    except:
        context = {'username': None}
    context = {'username': request.session.get('username')}
    context['role'] = request.session.get('role')
    
    try:
        products_response = requests.get(GET_ALL_PRODUCT_URL)
        if products_response.status_code == 200:
            products = products_response.json()
            context['products'] = products
        else:
            context['products'] = []
    except:
        context['products'] = []
    
    return render(request, 'productlist.html', context)

def cart_view(request):
    try:
        response = requests.get(USER_CHECK_URL, headers={'Authorization': 'Bearer ' + request.session.get('access_token')})
        if response.status_code == 401:
            return redirect('frontend:login')
    except:
        return redirect('frontend:login')
    username = request.session.get('username')
    if username is None:
        return redirect('frontend:login')
    context = {'buyer_username': username}
    access_token = request.session.get('access_token')
    response = requests.get(CART_URL, headers={'Authorization': 'Bearer ' + access_token})
    print(response.status_code)
    if response.status_code == 200:
        response_data = json.loads(response.text)
        print(response_data)
        cart_list = response_data
        print(cart_list) 
        context['cart_list'] = cart_list
    return render(request, 'carts.html', context)

def update_quantity(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cartId')
        quantity = int(request.POST.get('quantity'))
    try:
        response = requests.get(USER_CHECK_URL, headers={'Authorization': 'Bearer ' + request.session.get('access_token')})
        if response.status_code == 401:
            return redirect('frontend:login')
    except:
        return redirect('frontend:login')
    username = request.session.get('username')
    if username is None:
        return redirect('frontend:login')
    access_token = request.session.get('access_token')
    response = requests.put(UPDATE_QUANTITY_URL, data={'cartId': cart_id, 'quantity': int(quantity)}, headers={'Authorization': 'Bearer ' + access_token})
    if response.status_code == 200:
        return redirect('frontend:cart_view')
    else:
        error_message = "Failed to update quantity. Please try again."
        return JsonResponse({'error': error_message}, status=400)

def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')
        # productName = request.POST.get('productName')
        # price = request.POST.get('price')
    try:
            response = requests.get(USER_CHECK_URL, headers={'Authorization': 'Bearer ' + request.session.get('access_token')})
            if response.status_code == 401:
                return redirect('frontend:login')
    except:
            return redirect('frontend:login')
    username = request.session.get('username')
    if username is None:
        return redirect('frontend:login')
    access_token = request.session.get('access_token')
    quantity = 1
    response = requests.post(ADD_PRODUCT_URL, data={'productId': product_id, 'quantity':int(quantity)}, headers={'Authorization': 'Bearer ' + access_token})
    if response.status_code == 200:
        return redirect('frontend:cart_view')
    else:
        error_message = "Failed to add product. Please try again."
        return JsonResponse({'error': error_message}, status=400)

def checkout(request):
    selected_cart_ids = request.POST.getlist('selectedCartIds')
    print(selected_cart_ids)  # Print the selected cart IDs
    try:
            response = requests.get(USER_CHECK_URL, headers={'Authorization': 'Bearer ' + request.session.get('access_token')})
            if response.status_code == 401:
                return redirect('frontend:login')
    except:
            return redirect('frontend:login')
    username = request.session.get('username')
    if username is None:
        return redirect('frontend:login')
    access_token = request.session.get('access_token')
    response = requests.post(CHECKOUT_ORDER_URL, data={'username': username, 'cartProductsId':selected_cart_ids}, headers={'Authorization': 'Bearer ' + access_token})
    if response.status_code == 200:
        response_data = json.loads(response.text)
        order_id = response_data['id']
        print("masuk")
        print(order_id)
        return redirect('frontend:cart_view')
    else:
        error_message = "Failed to checkout product. Please try again."
        return JsonResponse({'error': error_message}, status=400)



  
  