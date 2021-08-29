from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .forms import CheckoutForm
from django.utils import timezone
from .models import Product, Order, OrderItem, ShippingAddress
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    context = {
        'products': Product.objects.all(),
        'title': 'Home'
    }
    return render(request, 'store/index.html', context)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, is_ordered=False)
        form = CheckoutForm()
        context = {
            'form': form,
            'object': order,
            'title': 'Checkout'
        }
        return render(self.request, "store/checkout.html", context)

    def post(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, is_ordered=False)
            form = CheckoutForm(self.request.POST)
            if form.is_valid():
                form.save()
                addr = ShippingAddress.objects.last()
                addr.user = self.request.user
                order.shipping_address = addr
                addr.save()
                order.save()
                return redirect("payment")
            messages.error(self.request, "Failed Checkout")
            return redirect("checkout")
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("cart")


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, is_ordered=False)
        context = {
            'object': order,
            'title': 'Payment'
        }
        return render(self.request, "store/payment.html", context)


def payment_intent(request):
    order = Order.objects.get(user=request.user, is_ordered=False)
    intent = stripe.PaymentIntent.create(
        amount=int((order.get_total() + 50) * 100),
        currency='inr',
    )
    return JsonResponse({'clientSecret': intent['client_secret']}, safe=True)


class SummaryView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, is_ordered=False)
        order.is_ordered = True
        order.save()
        context = {
            'object': order,
            'title': 'Order Confirmation'
        }
        return render(self.request, "store/order-summary.html", context)


class AllProductsView(ListView):
    model = Product
    template_name = 'store/products.html'
    paginate_by = 10


class ProductCategory(ListView):
    model = Product
    template_name = 'store/products.html'
    paginate_by = 10

    def get_queryset(self, **kwargs):
        return Product.objects.filter(category=self.kwargs['category'])

    def get_context_data(self, **kwargs):
        context = super(ProductCategory, self).get_context_data(**kwargs)
        lookup = {
            'L': 'Laptops',
            'S': 'Smartphones',
            'A': 'Accessories'
        }
        context['title'] = lookup[self.kwargs['category']]
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/single-product.html'


class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, is_ordered=False)
            context = {
                'object': order,
                'title': 'Cart'
            }
            return render(self.request, 'store/cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


@login_required
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
            return redirect("cart")
        else:
            messages.info(request, "This item was added to your cart")
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
    return redirect("product-specific", slug=slug)


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, is_ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from you cart")
            return redirect("cart")
        else:
            messages.info(request, "This item was not in your cart")
    else:
        messages.info(request, "You do not have an active order")
    return redirect("product-specific", slug=slug)


@login_required
def decrement_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, is_ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "Item quantity was updated!")
        else:
            messages.info(request, "This item was not in your cart")
    else:
        messages.info(request, "You do not have an active order")
    return redirect("cart")
