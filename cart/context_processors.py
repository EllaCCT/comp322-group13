##處理模版中上下文,確保每個模版都可訪問購物車
from .cart import Cart

def cart(request):
    return {'cart': Cart(request)}