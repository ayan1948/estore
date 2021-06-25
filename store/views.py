from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Product, Order, OrderItem


def home(request):
    return render(request, 'store/index.html')


class AllProductsView(ListView):
    model = Product
    template_name = 'store/products.html'


# def all_products(request):
#     context = {
#         'products': Product.objects.all()
#     }
#     return render(request, 'store/products.html', context)


# def product_type(request, kind):
#     context = {
#         'products': Product.objects.filter(category=kind).all()
#     }
#     return render(request, 'store/products.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/single-product.html'


def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, is_ordered=False)
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("product-specific", slug=slug)

# def product_detail(request, kind, specific):
#     context = {
#         'product': Product.objects.get(pk=specific)
#     }
#     return render(request, 'store/single-product.html', context)
