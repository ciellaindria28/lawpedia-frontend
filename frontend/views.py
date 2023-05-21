from django.shortcuts import render, redirect
import requests
from .endpoints import *
import json
from django.http import HttpResponse

# Create your views here.

def register_view(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            context = {'message': 'Passwords do not match'}
            return render(request, 'register.html', context)
        
        response = requests.post(REGISTER_URL, data={'username': username, 'email': email, 'password1': password1, 'password2': password2})
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
            username = response_data["data"]["username"]
            request.session['access_token'] = access_token
            request.session['refresh_token'] = refresh_token
            request.session['username'] = username
            return redirect('frontend:product_list')
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
    access_token = request.session.get('access_token')
    response = requests.get(GET_PDF_LIST, headers={'Authorization': 'Bearer ' + access_token})
    if response.status_code == 200:
        response_data = json.loads(response.text)
        pdf_list = response_data["data"]
        print(pdf_list)
        context['pdfs'] = pdf_list
    return render(request, 'download_orders.html', context)

def generate_pdf(request):
    access_token = request.session.get('access_token')
    response = requests.get(CREATE_PDF_URL, headers={'Authorization': 'Bearer ' + access_token})
    if response.status_code == 200:
        response_data = json.loads(response.text)
        message = response_data["data"]["message"]
        context = {'success': message, 'username': request.session.get('username')}
        return render(request, 'download_orders.html', context)
    else:
        context = {'message': 'Something went wrong'}
        return render(request, 'download_orders.html', context)
    
def download_pdf(request, pdf_id):
    access_token = request.session.get('access_token')
    response = requests.get(GET_PDF_RESULT_URL + f'?pdf_id={pdf_id}', headers={'Authorization': 'Bearer ' + access_token})
    if response.status_code == 200:
        # the response is a pdf file
        pdf = response.content

        # create a http response
        response = HttpResponse(pdf, content_type='application/pdf')
        return response
    else:
        context = {'message': 'Something went wrong'}
        return render(request, 'download_orders.html', context)
def add_product(request):
    return render(request,'productform.html')

def product_list(request):
    try:
        response = requests.get(USER_CHECK_URL, headers={'Authorization': 'Bearer ' + request.session.get('access_token')})
        if response.status_code == 401:
            context = {'username': None}
    except:
        context = {'username': None}
    context = {'username': request.session.get('username')}
    return render(request, 'productlist.html', context)

def cart_view(request):
    return render(request, 'cart_view.html')

def order_list(request):
    return render(request, 'order_list.html')

def order_detail(request):
    return render(request, 'order_detail.html')
