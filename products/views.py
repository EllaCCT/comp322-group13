from django.shortcuts import render
from products.models import Product
# Create your views here.
from django.views.generic import DetailView

#class ProductDetailView(DetailView):
    #model = Product
    #template_name = 'users/product_detail.html'
    #context_object_name = 'product'

def product_detail(request):
    #products=Product.objects.all()
    return render(request, 'products/product_detail.html')