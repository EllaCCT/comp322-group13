from django.views.generic import ListView , UpdateView, CreateView, DeleteView
from products.models import Product,ProductImage
from order.models import Order,OrderItem
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from django.forms import inlineformset_factory

ProductImageFormSet = inlineformset_factory(
                                Product,ProductImage,
                                fields=('image',),  # 只處理圖片字段
                                extra=4,            # 顯示4個上傳欄位
                                can_delete=False
                                )

OrderItemFormSet = inlineformset_factory(Order,OrderItem,
                                        fields=(),
                                        can_delete=False,
                                        extra=0  # 不顯示空白欄位
                                        )

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category','parent','name','price','description','is_show','stock', 'thumbnail','tag') # 依需調整字段
        widgets = {
            'description': CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, 
                config_name="default"  # 對應 settings.py 中的 CKEDITOR_5_CONFIGS
            ),
            'is_show' : forms.RadioSelect
        }

class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser
# Create your views here.

class ProductListView(SuperUserRequiredMixin,ListView):
    model = Product
    template_name = 'product_list.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(vendor=self.request.user)
        query = self.request.GET.get('query')
        if query:
            try:
                # 嘗試將 query 轉換為數字來搜索 ID
                queryset = queryset.filter(id__contains=query)
            except ValueError:
                # 若轉換失敗，則模糊搜索名稱
                queryset = queryset.filter(name__icontains=query)
        return queryset
        #return Product.objects.filter(vendor=self.request.user)
    
    def handle_no_permission(self):
        return HttpResponseForbidden('')

class ProductUpdateView(SuperUserRequiredMixin,UpdateView):
    model = Product
    #fields= ['name','price','description','is_show']
    form_class=ProductForm
    template_name = 'product_update.html'
    success_url = reverse_lazy('vendor_product_list')

    def handle_no_permission(self):
        return HttpResponseForbidden('')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ProductImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            context['image_formset'] = ProductImageFormSet(instance=self.object)
        return context
    
class AddProductView(SuperUserRequiredMixin,CreateView):
    model = Product
    #fields=['vendor','name', 'price', 'description','category']
    form_class=ProductForm
    template_name = 'product_add.html'
    success_url = reverse_lazy('vendor_product_list')

    def handle_no_permission(self):
        return HttpResponseForbidden('')
    
    #rewrite the 'POST' ,'GET' method
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ProductImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['image_formset'] = ProductImageFormSet()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']

        self.object = form.save(commit=False)
        self.object.vendor = self.request.user
        self.object.save()

        image_formset = ProductImageFormSet(
            self.request.POST,
            self.request.FILES,
            instance=self.object
        )
        if image_formset.is_valid():
            image_formset.save()
        else:
            return self.form_invalid(form)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form, image_formset=self.get_context_data()['image_formset'])
        )

class ProductDeleteView(SuperUserRequiredMixin,DeleteView):
    model = Product
    template_name = "product_delete.html"
    success_url = reverse_lazy('vendor_product_list')

    def handle_no_permission(self):
        return HttpResponseForbidden('')
 
class OrderListView(SuperUserRequiredMixin,ListView):
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'orders'

    def handle_no_permission(self):
        return HttpResponseForbidden('')
    
    def get_queryset(self): #目前此商家產品訂單
        return Order.objects.filter(items__product__vendor=self.request.user).distinct().order_by('-date_added')

class OrderUpdateView(SuperUserRequiredMixin,UpdateView):
    model = Order
    fields = ['status']
    template_name = 'order_update.html'
    success_url = reverse_lazy('vendor_order_list')

    def get_queryset(self):
        return Order.objects.filter(items__product__vendor=self.request.user).distinct()

    def handle_no_permission(self):
        return HttpResponseForbidden('')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.object  # 傳遞訂單對象到模板
        context['customer_name'] = self.object.user.get_full_name()  # 獲取用戶全名


        if self.request.POST:
            context['orderitem_formset'] = OrderItemFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context['orderitem_formset'] = OrderItemFormSet(instance=self.object)
        return context
        #context['items'] = self.object.items.all()
        #return context