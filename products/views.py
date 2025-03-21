from django.shortcuts import render, get_object_or_404
from products.models import Product
# Create your views here.
from django.views.generic import DetailView

#class ProductDetailView(DetailView):
    #model = Product
    #template_name = 'users/product_detail.html'
    #context_object_name = 'product'

def product_list(request):
    product = Product.objects.filter(is_show=True).prefetch_related('images')
    #product = Product.objects.all()
    return render(request, 'products/product_list.html', {'product': product})
    


def product_detail(request,slug):
    product= get_object_or_404(Product.objects.prefetch_related('images'), slug=slug)
        # 新增：获取同分类商品（排除当前商品）
    category_products = Product.objects.filter(
        category=product.category,
        is_show=True
    ).exclude(id=product.id).prefetch_related('images')[:4]  # 限制4个推荐商品
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'category_products': category_products  # 添加推荐商品到上下文
    })

