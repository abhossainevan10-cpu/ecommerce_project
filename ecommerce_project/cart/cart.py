from decimal import Decimal
from django.conf import settings
from products.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        pid = str(product.id)
        if pid not in self.cart:
            # দামটিকে স্ট্রিং হিসেবে রাখা হয়েছে যেন JSON সিরিয়ালাইজ করা যায়
            self.cart[pid] = {'quantity': 0, 'price': str(product.price)}
        
        if override_quantity:
            self.cart[pid]['quantity'] = quantity
        else:
            self.cart[pid]['quantity'] += quantity
        self.save()

    def save(self):
        # সেশন মডিফাইড ফ্ল্যাগ ট্রু করা যেন ডাটাবেসে সেভ হয়
        self.session.modified = True

    def remove(self, product):
        pid = str(product.id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        # মূল কার্ট ডাটা কপি করা হচ্ছে যেন সেশন অবজেক্ট মডিফাই না হয়
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            # ডেসিমাল কনভার্ট শুধু লুপ বা টেমপ্লেটে দেখানোর জন্য
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """সেশন থেকে কার্ট ডিলেট করা"""
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
            self.save()