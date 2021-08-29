from django.urls import path
from .views import home, AllProductsView, ProductDetailView, add_to_cart, ProductCategory, remove_from_cart, CartView, \
    decrement_from_cart, CheckoutView, PaymentView, payment_intent, SummaryView

urlpatterns = [
    path('', home, name='store-home'),
    path('allproducts/', AllProductsView.as_view(), name='all-products'),
    path('product-category/<category>', ProductCategory.as_view(), name='product-types'),
    path('cart/', CartView.as_view(), name='cart'),
    path('product/<slug>/', ProductDetailView.as_view(), name='product-specific'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('decrement-from-cart/<slug>/', decrement_from_cart, name='decrement-from-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('create-payment-intent/', payment_intent, name='create-payment-intent'),
    path('order-summary/', SummaryView.as_view(), name='order-summary')
]
