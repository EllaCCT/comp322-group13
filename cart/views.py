from django.shortcuts import render
from .cart import Cart
from products.models import Product

def add_to_cart(request, product_id):
    cart = Cart(request)
    #product_id = request.POST['product_id']
    product = Product.objects.get(id=product_id)

    cart.add(product_id)
    cart_quantity = cart.len(cart)  # 获取购物车中的商品数量
    return render(request, 'tmeplates/index.html')
