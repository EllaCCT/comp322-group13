from django.contrib import admin
from products.models import Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','price','is_show')
    search_fields = ('id','name')
    list_editable = ('is_show',)

admin.site.register(Product, ProductAdmin)