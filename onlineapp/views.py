import uuid
from django.db.models.query_utils import subclasses
# import requests
import json


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages


from onlineapp.forms import SignupForm
from . models import Category, Product, ShopCart,Payment

# Create your views

def index(request): 
    featured = Product.objects.filter(featured=True)
    latest = Product.objects.filter(latest=True)
    categories = Category.objects.all()

    context = {
        'featured': featured,
        'latest' : latest,
        'categories' : categories
    }
    
    return render(request, 'index.html',context)


def categories(request):
    categories=Category.objects.all()

    context={
        'categories': categories
    }

    return render(request, 'categories.html', context)

def single_category(request,id):
    category = Product.objects.filter(category_id=id)

    context={
        'category': category
    }

    return render(request,'category.html', context)

def products(request):
    products = Product.objects.all()

    context ={
        'products': products
    }

    return render(request, 'products.html', context)

def product(request,id):
    details = Product.objects.get(pk=id)

    context={
        'details': details 
    }

    return render(request, 'details.html', context)
    
def loginpage(request):  
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            login(request, user)
            messages.success(request, 'successful')
            return redirect('index')
        else:
            messages.info(request, 'username/password incorrect')
            return redirect('login')
    return render (request, 'login.html')



def logoutfunc(request):
    logout(request)
    return redirect('login')
    

def signupform(request):
    reg = SignupForm()
    if request.method == 'POST':
        reg = SignupForm(request.POST)
        if reg.is_valid():
            reg.save()
            messages.success(request, 'Signup successfull!')
            return redirect('index')
        else:
            messages.warning(request, reg.errors)
            return redirect ('signupform')

    context = {
        'reg': reg
    }

    return render (request, 'signup.html', context)



def password(request):
    update = PasswordChangeForm(request.user)
    if request.method == 'POST':
        update = PasswordChangeForm(request.user, request.POST)
        if update.is_valid():
            user=update.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password update successful!')
            return redirect('index')
        else:
            messages.error(request, update.errors)
            return redirect('password')

    context = {
        'update': update
    }

    return render(request, 'password.html', context)

def addtocart(request):
    if request.method == 'POST':
        basket_num =str(uuid.uuid4())
        vol = int(request.POST['quantity'])
        pid = request.POST['itemid']
        item = Product.objects.get(pk=pid)
        cart = ShopCart.objects.filter(user__username= request.user.username, paid_order=False)
        if cart:
            basket = ShopCart.objects.filter(user__username=request.user.username, product_id=item.id).first()
            if basket:
                basket.quantity += vol
                basket.save()
                messages.success(request,'product added to cart!')
                return redirect('products')
            else:
                    # this runs when a new item is added to the basket 
                newitem = ShopCart()
                newitem.user = request.user
                newitem.product =item
                newitem.basket_no = cart[0].basket_no
                newitem.quantity = vol
                newitem.paid_order = False
                newitem.save() 
                messages.success(request, 'Product added to cart !')
                    
        else:
            # this is when a basket is to be created for the first time 
            newbasket = ShopCart()
            newbasket.user = request.user
            newbasket.product =item
            newbasket.basket_no = basket_num
            newbasket.quantity = vol
            newbasket.paid_order = False
            newbasket.save() 
            messages.success(request, 'Product added to Basket !')
   
    return redirect('products')


def cart (request):
    cart = ShopCart.objects.filter(user__username=request.user.username, paid_order=False)

    cartreader = 0
    for item in cart :
        cartreader += item.quantity


    subtotal =0
    vat = 0
    total = 0

    for item in cart:
        subtotal += item.product.price * item.quantity

    vat = 0.075 * subtotal

    total = subtotal + vat

    context = {
        'cart': cart,
        'cartreader': cartreader,
        'subtotal': subtotal,
        'vat' : vat,
        'total': total
    }

    return render(request, 'cart.html', context)

def deleteitem(request):
    itemid=request.POST['itemid']
    ShopCart.objects.filter(pk=itemid).delete()
    messages.success(request, 'Product deleted')
    return redirect ('cart')


def increase(request):
    
    itemval=request.POST['itemval']
    if itemval < '1' :
        itemval= '1'
    valid=request.POST['valid']
    update=ShopCart.objects.get(pk=valid)
    update.quantity=itemval 

    update.save()
    messages.success(request, 'Product quantity update successfully')
    return redirect('cart')

def checkout (request):
    cart= ShopCart.objects.filter(user__username = request.user.username,paid_order=False)
    subtotal = 0
    vat = 0
    total = 0
    for item in cart:
        subtotal += item.product.price*item.quantity
        
        vat = 0.075 * subtotal

        total = subtotal + vat

    context = {
        'cart': cart,
        'total': total,
        'cartcode' : cart,
    }

    return render(request, 'checkout.html', context)

def placeorder(request):
    if request.method=='POST':
        api_key = 'sk_test_4b0e1d9d7d91ebed3107222a4dd563a987d740b3'
        curl= 'https://api.paystack.co/transaction/initialize'
        # cburl= 'http://52.14.69.207/completed'
        cburl= 'http://localhost:8000/completed'
        total= float(request.POST['total']) *100
        cart_code = request.POST['cart_code']
        pay_code= str(uuid.uuid4())
        user= User.objects.get(username=request.user.username)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']

       #collect data that you will send to paystack
        headers={'Authorization':f'Bearer {api_key}'}
        data={'reference':pay_code,'email':user.email,'amount':int(total),'callback_url':cburl,'basket_no':cart_code}

        #make a call to paystack
        try:
            r=request.post(curl, headers=headers, json=data)
        except Exception:
            messages.error(request, 'Network busy, try again')
            

        else:
            transback= json.loads(r.text)
            rd_url= transback['data']['authorization_url']

            paid = Payment ()
            paid.user=user 
            paid.amount=total 
            paid.basket_no=cart_code 
            paid.pay_code=pay_code 
            paid.paid_order=True
            paid.first_name = first_name  
            paid.last_name = last_name
            paid.phone = phone
            paid.save()

            bag = ShopCart.objects.filter(user__username=request.user, paid_order=False)
            for item in bag:
                item.paid_order=True
                item.save()

                stock=Product.objects.get(pk=item.product.id)
                stock.max -=item.quantity
                stock.save()
                
            return redirect(rd_url)
    return redirect('checkout')

def completed(request):
    user=User.objects.get(username=request.user.username)

    context={
        'user':user 
    }
    return render(request, 'completed.html', context)

