from django.db import models
from django.conf import settings

class Order(models.Model):
    PENDING= 'pending'
    ORDERED = 'ordered'
    SHIPPED = 'shipped'
    CANCELLED = 'cancelled'
    REFUNDED = 'refunded'

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ORDERED, 'Ordered'),
        (SHIPPED, 'Shipped'),
        (CANCELLED, 'Cancelled'),
        (REFUNDED, 'Refunded'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)
    #order_id = models.AutoField(max_length=50)
    
    date_added = models.DateTimeField(auto_now_add=True)
    shipping_address = models.CharField(max_length=200,default="", blank=True)
    phone = models.CharField(max_length=20, default="",blank=True)

    #訂單狀態
    status = models.CharField(max_length=50, choices=STATUS_CHOICES,default='ordered')
    
    # 訂單狀態變更日期
    shipment_date = models.DateTimeField(null=True, blank=True)
    cancellation_date = models.DateTimeField(null=True, blank=True)
    ticket_issue_date = models.DateTimeField(null=True, blank=True)
    refund_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['date_added']
        
    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())     

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', related_name='items',on_delete=models.CASCADE)
    price=models.PositiveIntegerField()
    quantity=models.PositiveIntegerField(default=1)

    #def get_total_price(self):
        #return self.price * self.quantity

    @property
    def total_price(self):
         return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity}*{self.product.name}"