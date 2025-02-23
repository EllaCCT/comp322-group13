from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .cart import Cart

def cart(request):
    return render(request, 'cart/cart.html')

@login_required() # 限制未登录用户不能访问
def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return render(request, 'cart/cart.html')

def add_to_cart(request, product_id):
    cart = Cart(request)
    #product_id = request.POST['product_id']
    #product = Product.objects.get(id=product_id)
    cart.add(product_id)
    
    #art_quantity = cart.len(cart)  # 获取购物车中的商品数量
    return render(request, 'tmeplates/index.html')