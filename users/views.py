from django.shortcuts import render
from products.models import Product,Category
#from django.views.generic import TemplateView

#class index(TemplateView):
    #template_name = 'users/index.html'

def index(request): 
    products=Product.objects.all()[0:8]
    return render(request, 'users/index.html', {'products':products})

def shop(request):
    categories=Category.objects.all()
    products=Product.objects.all()

    ###該分類內的玩具
    active_category = request.GET.get('category', '')
    if active_category:
        products = Product.objects.filter(category__slug=active_category)
    ###

    content = {
        'categories':categories,
        'products':products
    }

    return render(request, 'users/shop.html', content)
