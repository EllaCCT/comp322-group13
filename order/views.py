from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


from .models import Order
# Create your views here.

@login_required
def order_list(request):
    # 显示用户所有订单
    orders = Order.objects.filter(user=request.user).order_by('-date_added')
    return render(request, 'order/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    # 显示订单详情
    order = get_object_or_404(
        Order.objects.prefetch_related('items__product'), 
        id=order_id, 
        user=request.user)
    return render(request, 'order/order_detail.html',{'order': order})