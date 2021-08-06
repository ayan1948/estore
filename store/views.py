from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .forms import CheckoutForm
from django.utils import timezone
from .models import Product, Order, OrderItem, ShippingAddress


def home(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'store/index.html', context)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, is_ordered=False)
        form = CheckoutForm()
        context = {
            'form': form,
            'object': order
        }
        return render(self.request, "store/checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, is_ordered=False)
            if form.is_valid() and form.cleaned_data.get('save_info'):
                form.save()
                order.shipping_address = ShippingAddress.objects.filter(user=self.request.user)[-1]
                order.save()
                return redirect("payment")
            messages.error(self.request, "Failed Checkout")
            return redirect("checkout")
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("cart")


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


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/single-product.html'


class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, is_ordered=False)
            context = {
                'object': order
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
