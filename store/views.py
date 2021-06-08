from django.shortcuts import render
from .models import Product


def home(request):
    return render(request, 'store/index.html')


def all_products(request):
    products = Product.objects.all()
    return render(request, 'store/products.html', products)


def product_type(request, kind):
    products = Product.objects.filter(category=kind).all()
    return render(request, 'store/products.html', products)


def product_detail(request, specific):
    product = Product.objects.filter(id=specific)
    return render(request, 'store/single-product.html', product)
