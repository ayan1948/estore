from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = (
    ('L', 'Laptop'),
    ('S', 'Smartphone'),
    ('A', 'Accessories')
)


class Item(models.Model):
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=1)


class ModelNo(models.Model):
    title = models.CharField(max_length=30)
    serialNo = models.CharField(max_length=50)
    price = models.FloatField()
    screen = models.IntegerField()
    processor = models.CharField(max_length=50)
    ram = models.IntegerField()
    storage = models.CharField(max_length=10)
    OS = models.CharField(max_length=10)
    graphics = models.CharField(max_length=10)
    Specifications = models.TextField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    item = models.ForeignKey(ModelNo, on_delete=models.CASCADE)

    def __str__(self):
        return self.item


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
