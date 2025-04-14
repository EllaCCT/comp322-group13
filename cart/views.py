from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from products.models import Product,ProductAttributes
from order.models import Order, OrderItem
from .cart import Cart
from django.contrib import messages

def redirect_back(request, fallback_url='/'):
    """
    返回上一页或备用URL
    :param request: HttpRequest对象
    :param fallback_url: 当没有Referer时的默认跳转地址
    """
    referer = request.META.get('HTTP_REFERER')
    if referer:  # 安全验证（可选）
        # 如果需要防止开放重定向，可以添加域名验证：
        # if referer.startswith(settings.SITE_DOMAIN):
        return HttpResponseRedirect(referer)
    return redirect(fallback_url)

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


    if color or size:
        try:
            attr=ProductAttributes.objects.get(product=product, colors__color=color, sizes__size=size)
            if quantity > attr.stock:
                messages.error(request, "These group has not enough stock!")
                return redirect_back(request)
        except ProductAttributes.DoesNotExist:
            messages.error(request, "These group does not exist!")
            return redirect_back(request)
    else:
        if quantity > product.stock:
            messages.error(request, "Not enough stock!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

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
            
            if item.get('color')or item.get('size'):
                attr = ProductAttributes.objects.select_for_update().get(
                product=products,
                colors__color=item.get('color'),
                sizes__size=item.get('size')
                )
                attr.stock -= item['quantity'] # 扣減組合庫有
                attr.save()
            else:
                products.stock -= item['quantity']
                products.save()

            OrderItem.objects.create(
                order=order,
                product=products,
                price=item['price'],
                quantity=item['quantity'],
                color=item.get('color'),
                size=item.get('size')
                )
        cart.clear()
        return redirect('order_detail', order_id=order.id)
    
    initial_data = {}
    if hasattr(user, 'member'):
        initial_data['shipping_address'] = user.member.address
    
    return render(request, 'cart/checkout.html', {'initial_data': initial_data, 'cart': cart})
