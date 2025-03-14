from django.views.generic import ListView , UpdateView, CreateView
from products.models import Product
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden

# Create your views here.

class ProductListView(LoginRequiredMixin,ListView):
    model = Product
    template_name = 'product_list.html'

    def get_queryset(self):
        return Product.objects.filter(vendor=self.request.user)
    
    def handle_no_permission(self):
        return HttpResponseForbidden('')

class ProductUpdateView(LoginRequiredMixin,UpdateView):
    model = Product
    fields= [
        'name',
        'price',
        'description',
        'is_show'
    ]
    template_name = 'product_update.html'
    success_url = reverse_lazy('vendor_product_list')

    def handle_no_permission(self):
        return HttpResponseForbidden('')
    
class AddProductView(LoginRequiredMixin,CreateView):
    model = Product
    fields=[
        'vendor',
        'name',
        'price',
        'description',
        'category'
    ]
    template_name = 'product_add.html'
    success_url = reverse_lazy('vendor_product_list')