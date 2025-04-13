##處理模版中上下文,確保每個模版都可訪問購物車
from .cart import Cart

def cart(request):
    return {'cart': Cart(request)}

def cart_quantity(request):
    cart = Cart(request)
    return {
        'cart_quantity': sum(item['quantity'] for item in cart.cart.values())
    }