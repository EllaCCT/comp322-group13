from django.db.models import Q
from django.shortcuts import render
from products.models import Product,Category
#from django.views.generic import TemplateView

#class index(TemplateView):
    #template_name = 'users/index.html'

def index(request): 
    products=Product.objects.all()[0:8]
    return render(request, 'users/index.html', {'products':products})

def product(request):
    categories=Category.objects.all()
    products=Product.objects.all()

    ###該分類內的玩具
    active_category = request.GET.get('category', '')
    if active_category:
        products = products.filter(category__slug=active_category)

    query=request.GET.get('query','')
    
    if query: ##搜尋可以透過搜尋商品名稱或描述
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query)| Q(price__icontains=query))
            
        
    ###

    content = {
        'categories':categories,
        'products':products
    }

    return render(request, 'users/product.html', content)
