##設置session,客戶登入前可以將商品加入購物車
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

class Cart(object):
    def __init__(self,request):
        self.session =request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self,product,quantity=1,update_quantity=False):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':1,'id':product_id}

        if update_quantity:
            self.cart[product_id]['quantity'] += int(quantity)

            if self.cart[product_id]['quantity'] == 0:
                self.remove(product_id)
        self.save()

    def remove(self,product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    @property
    def items(self):
        """返回包含商品對象、數量、總價的列表"""
        items = []
        for product_id, item_data in self.cart.items():
            product = get_object_or_404(Product, id=int(product_id))

            total_price = product.price * item_data['quantity']

            thumbnail = None
            product_image = product.images.first()  # 使用反向關聯名稱 'images'
            if product_image and product_image.thumbnail:
                thumbnail = product_image.thumbnail.url

            items.append({
                'id': product_id,
                'product': product,
                'quantity': item_data['quantity'],
                'total_price': total_price,
                'price': product.price,
                'thumbnail': thumbnail,
                
            })
        return items

    @property
    def total_price(self):
        """計算購物車總金額"""
        return sum(item['total_price'] for item in self.items)