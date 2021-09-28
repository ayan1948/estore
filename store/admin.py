from django.contrib import admin

from .models import Laptop, Smartphone, Accessory, OrderItem, Order, ShippingAddress, Product

admin.site.register(Laptop)
admin.site.register(Smartphone)
admin.site.register(Accessory)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(ShippingAddress)
admin.site.register(Product)
