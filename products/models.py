from django.db import models
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug= models.SlugField(max_length=200)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='products',
                               null=True,
                               blank=True)
    #id=models.AutoField(primary_key=True,unique=True)
    category = models.ForeignKey(Category, related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = CKEditor5Field('Description')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    #image = models.ForeignKey.ImageField(upload_to='product', blank=True, null=True)
    #thumbnail = models.ImageField(upload_to='thumbnail/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_sale = models.BooleanField(verbose_name="hide product",default=False)
    is_show = models.BooleanField(verbose_name="show product",default=True)

    def __str__(self):
        return self.name
    
    
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='products/thumbnails', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Image'
        ordering= ['created_at']
    
    def __str__(self):
        return self.product.name
    
    def first_image(self):
        """获取第一个关联图片"""
        return self.images.first() 