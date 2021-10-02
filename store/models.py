from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.shortcuts import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
import json
import os

CATEGORY_CHOICES = (
    ('L', 'Laptop'),
    ('S', 'Smartphone'),
    ('A', 'Accessories')
)

files = os.listdir("./store/filters")
filters = {}
for file in files:
    with open(f"./store/filters/{file}") as f:
        filters[file] = json.load(f)


class Product(models.Model):
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=1)
    title = models.CharField(max_length=30)
    serialNo = models.CharField(max_length=50, blank=True)
    price = models.FloatField()
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='product_images')
    description = models.TextField(blank=True, null=True)

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 403 or img.width > 370:
            img.thumbnail((370, 403))
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse("product-specific", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })

    def remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'slug': self.slug
        })

    class Meta:
        db_table = 'Products'

    def __str__(self):
        return self.title


class Laptop(models.Model):
    brand = models.IntegerField(choices=filters['Laptop.json']['Brands'], default=None)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    screen = models.FloatField(default=None)
    processor = models.IntegerField(choices=filters['Laptop.json']['Processor'], default=None)
    ram = models.IntegerField(choices=filters['Laptop.json']['RAM'], default=None)
    storage = models.IntegerField(choices=filters['Laptop.json']['Storage'], default=None)
    OS = models.IntegerField(choices=filters['Laptop.json']['Operating System'], default=None)
    graphics = models.IntegerField(choices=filters['Laptop.json']['Graphics'], default=None)
    color = models.IntegerField(choices=filters['Laptop.json']['Color'], default=None)
    fingerprint = models.BooleanField(default=False)
    touchscreen = models.BooleanField(default=False)

    class Meta:
        db_table = 'Laptops'

    def __str__(self):
        return self.product.title


class Smartphone(models.Model):
    brand = models.IntegerField(choices=filters['Smartphone.json']['Brands'], default=None)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    screen = models.FloatField(default=None)
    processor = models.IntegerField(choices=filters['Smartphone.json']['Processor'], default=None)
    ram = models.IntegerField(choices=filters['Smartphone.json']['RAM'], default=None)
    storage = models.IntegerField(choices=filters['Smartphone.json']['Storage'], default=None)
    OS = models.IntegerField(choices=filters['Smartphone.json']['Operating System'], default=None)
    color = models.IntegerField(choices=filters['Smartphone.json']['Color'], default=None)
    frontcamera = models.IntegerField(choices=filters['Smartphone.json']['Front Camera'], default=None)
    backcamera = models.IntegerField(choices=filters['Smartphone.json']['Back Camera'], default=None)

    class Meta:
        db_table = 'Smartphones'

    def __str__(self):
        return self.product.title


class Accessory(models.Model):
    brand = models.IntegerField(choices=filters['Accessory.json']['Brands'], default=None)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        db_table = 'Accessories'

    def __str__(self):
        return self.product.title


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = '%s-%s' % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Product)


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False)

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_final_price(self):
        return self.get_total_item_price()

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    street_address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=20, null=True)
    zip = models.CharField(max_length=6, null=True)

    def __str__(self):
        return f'{self.user} Address'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField()
    is_ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)

    def get_total(self):
        total = 0
        for item in self.items.all():
            total += item.get_final_price()
        return total

    def __str__(self):
        return self.ordered_date
