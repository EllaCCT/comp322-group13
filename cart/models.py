from django.db import models
from products.models import Product
from django.contrib.auth.models import User

class Cart(models.Model):
    #----user=models.ForeignKey(User,on_delete=models.CASCADE)
    #-----cart_id = models.CharField(max_length=50)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'Cart'
        ordering = ['date_added']
        
    