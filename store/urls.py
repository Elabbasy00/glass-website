
from . import views
from django.urls import path

app_name = 'store'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product/<slug>/', views.ProductDetailView.as_view(), name="product_detail"),
    path('shop/', views.ShopView.as_view(), name="shop"),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('cart_update/', views.cart_update, name='cart_update'),
    path('cart/',views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout')
]
