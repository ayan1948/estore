from django.urls import path
from .views import home, AllProductsView, ProductDetailView, add_to_cart, product_category, remove_from_cart

urlpatterns = [
    path('', home, name='store-home'),
    path('allproducts/', AllProductsView.as_view(), name='all-products'),
    path('product-category/<category>', product_category, name='product-types'),
    path('product/<slug>/', ProductDetailView.as_view(), name='product-specific'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart')
]