from django.urls import path
from .views import home, all_products, product_type, product_detail

urlpatterns = [
    path('', home, name='store-home'),
    path('products/all/', all_products, name='all-products'),
    path('products/<kind>/', product_type, name='product-types'),
    path('products/<kind>/<int:specific>/', product_detail, name='product-specific'),
]
