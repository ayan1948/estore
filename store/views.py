from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Product, Order, OrderItem


def home(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'store/index.html', context)


class AllProductsView(ListView):
    model = Product
    template_name = 'store/products.html'
    paginate_by = 10


def product_category(request, category):
    context = {
        'object_list': Product.objects.filter(category=category)
    }
    return render(request, 'store/products.html', context)


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
            messages.info(request, "This item quantity was updated")
        else:
            messages.info(request, "This item was added to your cart")
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
    return redirect("product-specific", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item, created = OrderItem.objects.filter(item=item, user=request.user, is_ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from you cart")
        else:
            messages.info(request, "This item was not in your cart")
    else:
        messages.info(request, "You do not have an active order")
    return redirect("product-specific", slug=slug)

# def product_detail(request, kind, specific):
#     context = {
#         'product': Product.objects.get(pk=specific)
#     }
#     return render(request, 'store/single-product.html', context)
