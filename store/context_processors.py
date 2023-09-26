from .cart import Cart
from .models import Category
def basket(request):
    return {'cart':  Cart(request) }


def categories(request):
    return {
        'categories': Category.objects.all().prefetch_related("product_category")
    }