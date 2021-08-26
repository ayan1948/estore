# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from django.dispatch import receiver
# from .models import ShippingAddress, Order
#
#
# @receiver(post_save, sender=Order)
# def create_order(sender, instance, created, **kwargs):
#     if created:
#         ShippingAddress.objects.create(user=instance.user)
#
#
# @receiver(post_save, sender=Order)
# def save_order(sender, instance, **kwargs):
#     instance.shippingaddress.save()
