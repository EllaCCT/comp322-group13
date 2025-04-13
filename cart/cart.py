from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

class Cart(object):
    def __init__(self, request):
        self.session = request.session
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

    def add(self, product, quantity=1, update_quantity=False, color=None, size=None):
        # 生成唯一鍵，考慮產品ID、顏色和尺寸
        key = self._generate_cart_key(product.id, color, size)
        
        if key not in self.cart:
            self.cart[key] = {
                'product_id': str(product.id),
                'quantity': max(quantity, 1),
                'price': str(product.price),
                'color': color,
                'size': size
            }
        else:
            if update_quantity:
                self.cart[key]['quantity'] += quantity
            else:
                self.cart[key]['quantity'] = quantity

        if self.cart[key]['quantity'] < 1:
            self.remove(key)
        self.save()

    def _generate_cart_key(self, product_id, color, size):
        """生成購物車項目的唯一鍵，考慮產品ID、顏色和尺寸"""
        key_parts = [str(product_id)]
        if color:
            key_parts.append(str(color))
        if size:
            key_parts.append(str(size))
        return ':'.join(key_parts)

    def remove(self, cart_key):
        if cart_key in self.cart:
            del self.cart[cart_key]
            self.save()

    @property
    def items(self):
        """返回包含商品對象、數量、總價的列表"""
        items = []
        for cart_key, item_data in self.cart.items():
            product = get_object_or_404(Product, id=int(item_data['product_id']))
            
            total_price = product.price * item_data['quantity']

            thumbnail = product.thumbnail

            items.append({
                'id': cart_key,
                'product': product,
                'quantity': item_data['quantity'],
                'total_price': total_price,
                'price': product.price,
                'thumbnail': thumbnail,
                'color': item_data.get('color'),
                'size': item_data.get('size')
            })
        return items

    @property
    def total_price(self):
        """計算購物車總金額"""
        return sum(item['total_price'] for item in self.items)
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_price(self):
        return sum(float(item['product'].price) * item['quantity'] for item in self.items)
