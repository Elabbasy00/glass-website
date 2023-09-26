from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Product, Slider, Category
from accounts.models import User, Address
import json
from django.http import JsonResponse, HttpResponseRedirect
from .cart import Cart
import ast
from django.contrib.auth.decorators import login_required
# Create your views here.

class HomeView(ListView):
    model = Product
    template_name = 'store/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['slides'] = Slider.objects.all()
        context['categorys'] = Category.objects.all().prefetch_related("product_category")
        context['on_sale'] = Product.objects.filter(is_active=True, discount_price__isnull=False).prefetch_related('product_images')

        return context

    def get_queryset(self):
        return Product.objects.filter(is_active=True,discount_price__isnull=True).prefetch_related('product_images')



class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product-detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(is_active=True, category__name=self.object.category.name).prefetch_related('product_images').select_related('category').exclude(id=self.object.id)[:6]
        return context



class ShopView(ListView):
    model = Product
    template_name = 'store/shop.html'
    context_object_name = 'products'
    paginate_by = 20
    def get_context_data(self, **kwargs):
        context = super(ShopView, self).get_context_data(**kwargs)
        filter_set = Product.objects.filter(is_active=True).prefetch_related('product_images').select_related('category')
    
        if self.request.GET.get('category'):
            category = self.request.GET.get('category')
            price = self.request.GET.get('price')
            
            
            filter_set = filter_set.filter(category__slug=category).prefetch_related('product_images').select_related('category')


        context['products'] = filter_set
        return context

    def get_queryset(self):
        return Product.objects.filter(is_active=True,discount_price__isnull=True).prefetch_related('product_images').select_related('category')

def add_to_cart(request):
    cart = Cart(request)
    if request.method == 'POST':
        data = ast.literal_eval(request.POST.get('variation'))
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')
        product = get_object_or_404(Product.objects.select_related('category'), id=product_id)
        print(data)
        success, errorMsg = product.has_vars(data, request)
        if success:
            added = cart.add(product=product, product_qty=product_qty, variation=data)
            total_price = cart.get_total_price()
            added_product = None
            if added:
                added_product = cart.get_added_product(product=product, variation=data)
            return JsonResponse({'qty': len(cart), 'total_price': total_price, 'added_product': added_product})
        else:
            return JsonResponse({"errorMsg": errorMsg}, status=400)

  


def remove_from_cart(request):
    cart = Cart(request)
    if request.method == 'POST':
        data = ast.literal_eval(request.POST.get('data'))
        product_id = request.POST.get('product_id')
        cart.delete(product=product_id, variation=data)
        total_price = cart.get_total_price()
        return JsonResponse({'qty': len(cart), 'total_price': total_price})



def cart_update(request):
    cart = Cart(request)
    if request.method == 'POST':
        data = ast.literal_eval(request.POST.get('data'))
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')
        product = get_object_or_404(Product.objects.prefetch_related( 'product_variation', 'product_images').select_related('category'), id=product_id)

        updated_product = cart.update(product=product, product_qty=product_qty, variation=data)
        total_price = cart.get_total_price()
        return JsonResponse({'qty': len(cart), 'total_price': total_price, 'product_total_price': updated_product['product_total'], 'variation': updated_product['variation']})


def cart(request):
    return render(request, 'store/cart.html')
    

@login_required()   
def checkout(request):
    user_address = Address.objects.filter(user_id=request.user.id)
    shipping_diffrent = request.POST
    # print(shipping_diffrent)
    # TODO : check if user have an shipping and billing address
    # TODO : return defaults if exist + others
    # --------
    # TODO : Check for action defaults in request to handel order with default address
    # TODO : check for action exist but not default 
    # TODO : check for new address
    return render(request, 'store/checkout.html', context={"addresses": user_address})