from django.urls import path
from .views import home, AllProductsView, ProductDetailView, add_to_cart

urlpatterns = [
    path('', home, name='store-home'),
    path('allproducts/', AllProductsView.as_view(), name='all-products'),
    # path('products/<str:kind>/', product_type, name='product-types'),
    path('products/<slug>/', ProductDetailView.as_view(), name='product-specific'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart')
]
