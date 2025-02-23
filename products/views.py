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
    return render(request, 'products/product_detail.html',{'product':product})