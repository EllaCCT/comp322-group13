from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug= models.SlugField(max_length=200)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class Product(models.Model):
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='products',
                               null=True,
                               blank=True,
                               limit_choices_to={"is_staff": True})
    #id=models.AutoField(primary_key=True,unique=True)
    parent = models.ForeignKey("self", related_name='variants',on_delete=models.CASCADE, null=True, blank=True,limit_choices_to={"parent":None})
    category = models.ForeignKey(Category, related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = CKEditor5Field('Description')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    #image = models.ForeignKey.ImageField(upload_to='product', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='products/thumbnails', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_show = models.BooleanField(verbose_name="show/hide product",default=True)
    stock = models.PositiveIntegerField(null=False,blank=False)
    #color = models.ManyToManyField(Color)
    #size = models.ManyToManyField(Size)
    tag = TaggableManager()

    def instock(self):
        return self.stock
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
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