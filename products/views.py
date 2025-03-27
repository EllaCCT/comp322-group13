from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from products.models import Product, Category
# Create your views here.
from django.views.generic import DetailView
from django.shortcuts import redirect

#class ProductDetailView(DetailView):
    #model = Product
    #template_name = 'users/product_detail.html'
    #context_object_name = 'product'

# def product_list(request):
    # product = Product.objects.filter(is_show=True).prefetch_related('images')
    #product = Product.objects.all()
    # return render(request, 'products/product_list.html', {'product': product})

#def product_detail(request,slug):
    #product= get_object_or_404(Product.objects.prefetch_related('images'), slug=slug)
    #return render(request, 'products/product_detail.html',{'product':product})

def product_list(request):
    products = Product.objects.filter(parent=None).filter(is_show=True).prefetch_related('images')
    
    categories=Category.objects.all()    

    ###該分類內的玩具
    active_category = request.GET.get('category', '')
    if active_category:
        products = products.filter(category__slug=active_category)

    query=request.GET.get('query','')
    
    if query: ##搜尋可以透過搜尋商品名稱或描述
        products = products.filter(Q(name__icontains=query)|Q(description__icontains=query)|Q(price__icontains=query)|Q(tag__icontains=query)) 
    ###

    content = {
        'categories':categories,
        'products':products
    }
    
    return render(request, 'products/product.html', content)

def product_detail(request,slug):
    product= get_object_or_404(Product.objects.prefetch_related('images', 'variants__images', ), slug=slug)
    
    if product.parent:
        return redirect('', slug=product.parent.slug)
    
    # 获取同分类商品（排除当前商品）
    same_category = Product.objects.filter(
        parent=None,
        category=product.category,
        is_show=True
    ).exclude(id=product.id).prefetch_related('images')
    
    # 获取其他分类商品（当同分类不足4个时补充）
    other_category = Product.objects.exclude(
        category=product.category
    ).exclude(id=product.id).filter(is_show=True).prefetch_related('images')
    
    # 合并两个查询集并限制4个
    category_products = list(same_category[:4]) 
    if len(category_products) < 4:
        needed = 4 - len(category_products)
        category_products += list(other_category[:needed])
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'category_products': category_products[:4]  # 确保最多4个
    })