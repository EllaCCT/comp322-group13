from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from products.models import Product

from .cart import Cart

def cart(request):
    cart = Cart(request) 
    return render(request, 'cart/cart.html',context={'cart':cart})

#@login_required() # 限制未登录用户不能访问

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect( 'cart')

def add_to_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.add(product)
    return redirect('cart')

def checkout(request):
    return render(request, 'cart/checkout.html')