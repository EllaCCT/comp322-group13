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
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #order_id = models.AutoField(max_length=50)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

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
        return self.order_id
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', related_name='items',on_delete=models.CASCADE)
    price=models.PositiveIntegerField()
    quantity=models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.price * self.quantity