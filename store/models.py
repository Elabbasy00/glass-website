from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Address
from django.shortcuts import get_object_or_404

User = get_user_model()


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

TYPE_CHOICES = (
    ('SELECT', 'Select Box'),
    ('RADIO', 'Radio Choices'),

)

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    category_image = models.ImageField(upload_to='images/category_image/')

    class Meta:
        verbose_name_plural = 'categories'

    # def get_absolute_url(self):
    #     return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name




class Slider(models.Model):
    title = models.CharField(max_length=150, null=True, blank=True)
    sub_title = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/slidess/')

    def __str__(self):
        return "{}".format(self.id)




class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    slug = models.SlugField()
    description = models.TextField()
    small_description = models.TextField(null=True, blank=True)
    sku = models.CharField(max_length=100, null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    count_sold = models.IntegerField(default=0, verbose_name=('count sold'))
    available_quantity =  models.IntegerField(default=0, verbose_name=('available quantity'))
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("store:product_detail", kwargs={
            'slug': self.slug
        })
        
    def save(self, *args, **kwargs):
        product_vars = self.product_variation.all()
        if product_vars:
            total_qty = 0
            for var in product_vars:
                for qty in var.product_variation_info.all():
                    total_qty += qty.available_quantity
            if total_qty <= 0:
                self.is_active = False;
        elif self.available_quantity <=0:
            self.is_active = False
        else:
            self.is_active = True

        return super(Product, self).save(*args, **kwargs)

    def has_vars(self, data, request):
        print("data")
        if(data):
            related_vars = self.product_variation.filter(name__in=data.keys()).all()
            for var in related_vars:
                current_values = var.product_variation_info.filter(value__in=data.values()).all()
                for value in current_values:
                    if value.available_quantity <= 0:
                        return False, "{} {} Dont have Any Quantity ".format(value.value, var.name)
        elif self.available_quantity <= 0:
          
            return False , "Dont have Any Quantity "


class ProductMedia(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to='images/products/')



class Variation(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_variation")
    name = models.CharField(max_length=50)  # size
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='SELECT')

    class Meta:
        unique_together = (
            ('item', 'name')
        )
        
    def __str__(self):
        return self.name


class ProductVariation(models.Model):
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE, related_name="product_variation_info")
    value = models.CharField(max_length=50) 
    attachment = models.ImageField(upload_to="images/products/product_variation/",blank=True, null=True)
    available_quantity =  models.IntegerField(default=0, verbose_name=('available quantity'))


    class Meta:
        unique_together = (
            ('variation', 'value')
        )
        ordering = ['id']
        
    def __str__(self):
        return self.value
    


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    item_variations = models.ManyToManyField(ProductVariation)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        Address, related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        Address, related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    # payment = models.ForeignKey(
    #     'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    # refund_requested = models.BooleanField(default=False)
    # refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        # if self.coupon:
        #     total -= self.coupon.amount
        return total


