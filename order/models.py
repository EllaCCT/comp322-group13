from django.db import models
from django.conf import settings
from django.utils import timezone

class Order(models.Model): 
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Ordered', 'Ordered'),
        ('Shipped', 'Shipped'),
        ('Cancelled', 'Cancelled'),
        ('Refunded', 'Refunded'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)
    #order_id = models.AutoField(max_length=50)
    shipping_address = models.CharField(max_length=200,default="", blank=True)
    phone = models.CharField(max_length=20, default="",blank=True)

    #訂單狀態
    status = models.CharField(max_length=50, choices=STATUS_CHOICES,default='Ordered')
    
    # 訂單狀態變更日期
    date_added = models.DateTimeField(auto_now_add=True)
    shipment_date = models.DateTimeField(null=True, blank=True)
    cancellation_date = models.DateTimeField(null=True, blank=True)
    refund_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['date_added']
        
    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
    
    # 在 Order 模型的 save() 方法中
    def save(self, *args, **kwargs):
        if self.status == 'Shipped' and not self.shipment_date:
            self.shipment_date = timezone.now()
            self.cancellation_date = None
            self.refund_date = None
        elif self.status == 'Cancelled' and not self.cancellation_date:
            self.cancellation_date = timezone.now()
            self.shipment_date = None
        elif self.status == 'Refunded' and not self.refund_date:
            self.refund_date = timezone.now()
            self.shipment_date = None
    # 其他狀態同理

        if not self.pk:  # 連接shipping_address=member.address
            if self.user and hasattr(self.user, 'member'):
                self.shipping_address = self.user.member.address
        super().save(*args, **kwargs)
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())     

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', related_name='items',on_delete=models.CASCADE)
    price=models.PositiveIntegerField()
    quantity=models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10,null=True,blank=True,editable=False)
    color = models.CharField(max_length=20,null=True,blank=True,editable=False)

    #def get_total_price(self):
        #return self.price * self.quantity

    @property
    def total_price(self):
         return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity}*{self.product.name}"