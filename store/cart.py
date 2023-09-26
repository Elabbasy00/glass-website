from decimal import *
from .models import Product, Order, OrderItem
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

class Cart():

    """
        A base Cart class, providing some default behaviors that
        can be inherited or overrided, as necessary.
        
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if 'cart' not in request.session:
            cart = self.session['cart'] = {}
        self.cart = cart


    def add(self, product, product_qty, variation):
        """
            adding and updating the users basket session data
        """
        product_id = str(product.id)
        if(product.discount_price):
            product_price = str(product.discount_price)
        else:
            product_price = str(product.price)

        added = False
        if product_id not in self.cart:
            self.cart[product_id] = { 'price': product_price, 'qty_per_variation': (int(product_qty),), 'variation': (variation,) }
            added =  True
        elif product_id in self.cart and variation  not in self.cart[product_id]['variation']:
            self.cart[product_id]['variation'].append(variation)
            self.cart[product_id]['qty_per_variation'].append(int(product_qty))
            added =  True

        elif product_id in self.cart and variation in self.cart[product_id]['variation']:
            for var in range(len(self.cart[product_id]['variation'])):
                if self.cart[product_id]['variation'][var] == variation:
                    self.cart[product_id]['qty_per_variation'][var] = int(product_qty)
                    added = False
        self.save()
        return added

    
    def delete(self, product, variation):
        """
            Delete Item from session data
        """
        product_id = str(product)
        variation.pop('qty_per_variation', None)

        if product_id in self.cart and len(self.cart[product_id]['variation']) <= 1:
            del self.cart[product_id]
            self.save()

        elif product_id in self.cart and len(self.cart[product_id]['variation']) > 1:
            for var in range(len(self.cart[product_id]['variation'])):
                if self.cart[product_id]['variation'][var] == variation:
                    del self.cart[product_id]['variation'][var]
                    del self.cart[product_id]['qty_per_variation'][var]
                    self.save()
                    return True



    def update(self, product, product_qty, variation):
        """
            update session values
        """
        
        product_id = str(product.id)
        variation.pop('qty_per_variation', None)

        if product_id in self.cart and variation in self.cart[product_id]['variation']:
            for var in range(len(self.cart[product_id]['variation'])):
                if self.cart[product_id]['variation'][var] == variation:
                    self.cart[product_id]['qty_per_variation'][var] = int(product_qty)
                    self.save()
                    product_total = Decimal(self.cart[product_id]['price']) * self.cart[product_id]['qty_per_variation'][var]
                    new_variation = self.cart[product_id]['variation'][var]
                    return {"product_total":product_total.quantize(Decimal('.01'), rounding=ROUND_UP) , "variation": new_variation}
        else:
            print("error, ", variation) 


    def __len__(self):
        """
            get cart data and count the qty of items
        """
        return sum( var for item in self.cart.values() for var in item['qty_per_variation'] )
    
    def __iter__(self):
        """
            collect the products ids from session data to query the database
            and return products
        """
        products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=products_ids).prefetch_related( 'product_variation', 'product_images').select_related('category')
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            for var in range(len(item['variation'])):
                item['variation'][var]['qty_per_variation'] = item['qty_per_variation'][var]
            yield item

    
    def get_total_price(self):
        total =  Decimal(sum(Decimal(item['price']) * item['qty_per_variation'][var] for item in self.cart.values() for var in range(len(item['variation'])))) 
        return total.quantize(Decimal('.01'), rounding=ROUND_UP)
    

    def get_added_product(self, product, variation):
        product_id = str(product.id)
        copy = self.cart.copy()
        to_return = {}
        if product_id in copy and variation in copy[product_id]['variation']:
            for var in range(len(copy[product_id]['variation'])):
                if copy[product_id]['variation'][var] == variation:
                    to_return['product'] = model_to_dict(product)
                    to_return['variation'] = copy[product_id]['variation'][var]
                    to_return['qty_per_variation'] = copy[product_id]['qty_per_variation'][var]
                    return to_return



    def save(self):
        self.session.modified = True


    