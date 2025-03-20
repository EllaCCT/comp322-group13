from django.contrib import admin
from products.models import Product,ProductImage
from order.models import Order
from django.utils.safestring import mark_safe

class ProductImageInline(admin.TabularInline):
    model=ProductImage
    extra = 4
    readonly_fields=['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px; max-width: 100px;" />')
        return "-"
    image_preview.short_description = 'Preview'
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','price','is_show','is_sale')
    search_fields = ('id','name')
    list_editable = ('is_show','is_sale')
    inlines = [ProductImageInline,]

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'date_added')
    #inlines = [OrderItemInline] 

    

admin.site.register(Product, ProductAdmin)
admin.site.register(Order)