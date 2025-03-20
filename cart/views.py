from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from products.models import Product

from order.models import Order, OrderItem
from products.models import Product
from users.models import Member
from .cart import Cart

@login_required(login_url='/login/')
def cart(request):
    cart = Cart(request) 
    return render(request, 'cart/cart.html',context={'cart':cart})

#@login_required() # 限制未登录用户不能访问
def update_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    action = request.POST.get('action')

    if action == 'increase':
        cart.add(product, 1, True)
    elif action == 'decrease':
        # 减少数量时，若当前数量为1则移除商品
        current_quantity = cart.cart.get(str(product_id), {}).get('quantity', 0)
        if current_quantity <= 1:
            cart.remove(product_id)
        else:
            cart.add(product, -1, True)
    
    return redirect('cart')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect( 'cart')

def add_to_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    quantity = int(request.POST.get('quantity', 1)) 
    cart.add(product, quantity=quantity)
    return redirect('cart')

@login_required
def checkout(request):
    cart = Cart(request)
    user = request.user

    # 关键修改：创建订单逻辑
    if request.method == 'POST':
        # 验证购物车非空
        if not cart.items:
            return redirect('cart')
        
       # 创建订单（不再关联 product）
        order = Order.objects.create(
            user=request.user,
            shipping_address=request.POST.get('shipping_address', '')
        )
        
        # 通过 OrderItem 关联商品
        for item in cart.items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
        
        cart.clear()
        return redirect('order_detail', order_id=order.id)
    
    initial_data = {} #關聯地址
    if hasattr(user, 'member'):
        initial_data['shipping_address'] = user.member.address
    
    return render(request, 'cart/checkout.html', {'initial_data': initial_data, 'cart': cart})
