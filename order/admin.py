from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'price', 'quantity', 'total_price']
    readonly_fields = ['total_price']
    extra = 0

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

#@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['id', 'user','total_price',]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'price', 'order']
    search_fields = ['product__name', 'order__id']
    readonly_fields = ['color','size','total_price']