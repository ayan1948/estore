from django.contrib import admin

from .models import Item, OrderItem, Order, ModelNo

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(ModelNo)