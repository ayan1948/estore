from django.contrib import admin

from .models import Product, OrderItem, Order, ShippingAddress

admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(ShippingAddress)
