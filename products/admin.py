from django.contrib import admin
from .models import Category,Product,ProductImage
from django.utils.safestring import mark_safe


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 4
    readonly_fields=['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px; max-width: 100px;" />')
        return "-"
    image_preview.short_description = 'Preview'

class ProductAdmin(admin.ModelAdmin):
    #list_display = ('id', 'name', 'category', 'price', 'is_show', 'is_sale')
    search_fields = ['id', 'name', 'category__name']
    inlines = [ProductImageInline,]

    readonly_fields = ['id']
    
admin.site.register(Category)
#admin.site.register(Product,ProductAdmin)
#admin.site.register(ProductImage)

