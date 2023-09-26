from django.contrib import admin
from .models import (
    Category, Slider, Product, ProductMedia, Variation, ProductVariation,
     OrderItem, Order
)
# Register your models here.

class MediaInline(admin.StackedInline):
    model = ProductMedia

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    # 'refund_requested',
                    # 'refund_granted',
                    'shipping_address',
                    'billing_address',
                    # 'payment',
                    # 'coupon'
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
        # 'payment',
        # 'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                #    'refund_requested',
                #    'refund_granted'
                   ]
    search_fields = [
        'user__username',
        'ref_code'
    ]





class ItemVariationAdmin(admin.ModelAdmin):
    list_display = ['variation',
                    'value',
                    'attachment']
    list_filter = ['variation', 'variation__item']
    search_fields = ['value']


class ItemVariationInLineAdmin(admin.TabularInline):
    model = ProductVariation
    extra = 1


class VariationAdmin(admin.ModelAdmin):
    list_display = ['item',
                    'name']
    list_filter = ['item']
    search_fields = ['name']
    inlines = [ItemVariationInLineAdmin]

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'price', 'discount_price']
    list_editable = ['price', 'discount_price']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [MediaInline]



admin.site.register(ProductVariation, ItemVariationAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Slider)
admin.site.register(Category)

