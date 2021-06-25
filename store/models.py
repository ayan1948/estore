from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.shortcuts import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify

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
    graphics = models.CharField(max_length=10, null=True)
    color = models.CharField(max_length=10)
    frontcamera = models.CharField(max_length=10, blank=True)
    backcamera = models.CharField(max_length=10, blank=True)
    specifications = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(default='default.jpg', upload_to='product_images')

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            img.thumbnail((500, 500))
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse("product-specific", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart(self):
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })

    def __str__(self):
        return self.title


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


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField
    ordered_date = models.DateTimeField()
    is_ordered = models.BooleanField(default=False)


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
