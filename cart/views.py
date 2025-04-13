from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from products.models import Product
from order.models import Order, OrderItem
from .cart import Cart
from django.contrib import messages

@login_required(login_url='/login/')
def cart(request):
    cart = Cart(request)
    cart_quantity = sum(item['quantity'] for item in cart.cart.values())
    return render(request, 'cart/cart.html', context={
        'cart': cart,
        'cart_quantity': cart_quantity
    })


def update_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    action = request.POST.get('action')
    color = request.POST.get('color', None)  # 獲取顏色參數，默認為None
    size = request.POST.get('size', None)    # 獲取尺寸參數，默認為None

    # 使用相同的邏輯生成購物車鍵
    if action == 'increase':
        cart.add(product, quantity=1, update_quantity=True, color=color, size=size)
    elif action == 'decrease':
        # 獲取當前項目的數量
        cart_key = cart._generate_cart_key(product_id, color, size)
        current_quantity = cart.cart.get(cart_key, {}).get('quantity', 0)
        
        if current_quantity <= 1:
            cart.remove(cart_key)
        else:
            cart.add(product, quantity=-1, update_quantity=True, color=color, size=size)
    
    return redirect('cart')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    color = request.POST.get('color', None)
    size = request.POST.get('size', None)
    
    # 生成與添加時相同的鍵
    cart_key = cart._generate_cart_key(product_id, color, size)
    cart.remove(cart_key)
    
    return redirect('cart')

def add_to_cart(request, product_id):
    cart = Cart(request)
    selected_product_id = request.POST.get('product_id', product_id)
    product = get_object_or_404(Product, id=selected_product_id)
    quantity = int(request.POST.get('quantity', 1)) 
    color = request.POST.get('color')
    size = request.POST.get('size')

    if quantity > product.stock:
        messages.error(request, "Not enough stock!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        cart.add(product, quantity=quantity, color=color, size=size)
        return redirect('cart')

@login_required
def checkout(request):
    cart = Cart(request)
    user = request.user

    if request.method == 'POST':
        if not cart.items:
            return redirect('cart')
        
        for item in cart.items:
            products = Product.objects.get(id=item['product'].id)
            quantity = item['quantity']
            if (quantity > products.stock):                
                return redirect('cart')
        
        order = Order.objects.create(
            user=request.user,
            shipping_address=request.POST.get('shipping_address', '')
        )

        for item in cart.items:
            products = Product.objects.get(id=item['product'].id)
            quantity = item['quantity']
            if(products.stock > quantity):
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=quantity,
                    color=item.get('color'),
                    size=item.get('size')
                )
                products.stock -= quantity
                products.save()

        cart.clear()
        return redirect('order_detail', order_id=order.id)
    
    initial_data = {}
    if hasattr(user, 'member'):
        initial_data['shipping_address'] = user.member.address
    
    return render(request, 'cart/checkout.html', {'initial_data': initial_data, 'cart': cart})
