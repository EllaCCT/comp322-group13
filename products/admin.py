from django.contrib import admin
from .models import *
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

class ProductAttributesInline(admin.StackedInline):
    model = ProductAttributes
    extra = 3  

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'is_show')
    search_fields = ['id', 'name', 'category__name']
    inlines = [
        ProductAttributesInline,
        ProductImageInline
        ]
    readonly_fields = ['id']

class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Color)
admin.site.register(Size)
#admin.site.register(ProductImage)

