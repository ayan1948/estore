from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

CATEGORY_CHOICES = (
    ('L', 'Laptop'),
    ('S', 'Smartphone'),
    ('A', 'Accessories')
)


class Product(models.Model):
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=1)
    title = models.CharField(max_length=30)
    serialNo = models.CharField(max_length=50)
    price = models.FloatField()
    screen = models.IntegerField()
    processor = models.CharField(max_length=50)
    ram = models.IntegerField()
    storage = models.CharField(max_length=10)
    OS = models.CharField(max_length=10)
    graphics = models.CharField(max_length=10)
    color = models.CharField(max_length=10)
    frontcamera = models.CharField(max_length=10)
    backcamera = models.CharField(max_length=10)
    specifications = models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='product_images')

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            img.thumbnail((500, 500))
            img.save(self.image.path)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)


class OrderItem(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.item
