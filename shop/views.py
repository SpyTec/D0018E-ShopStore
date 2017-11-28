from itertools import product

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import generic
from shop.models import Product, Category, CartItem, Cart
from order.models import Order, OrderProduct
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


class Overview(generic.ListView):
    template_name = 'shop/list.html'
    model = Product


class ProductView(generic.DetailView):
    template_name = 'shop/detail.html'
    model = Product


class CategoryView(generic.DetailView):
    template_name = 'shop/list_category.html'
    model = Category


class CategoryOverview(generic.ListView):
    template_name = 'shop/shop_base.html'
    model = Category


@login_required()
def add_to_cart(request, pk):
    # Get current user and product
    current_user = request.user
    product = Product.objects.get(pk=pk)

    # Look if user has existing cart
    cart_count = Cart.objects.filter(user=current_user).count()
    if cart_count is 0:
        # Create new cart
        cart = Cart(user=current_user)
        cart.save()
    else:
        # Use existing cart for user
        cart = Cart.objects.get(user=current_user)

    # Create snapshot and add to user basket
    article, created = CartItem.objects.get_or_create(product=product, user_cart=cart)
    article.price_snapshot = product.price
    if request.POST.get("quantity").isdigit():
        article.quantity = request.POST.get("quantity", "1")
    else:
        article.quantity = 1
    article.save()

    messages.info(request, "{} has been added to cart.".format(product.name))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required()
def checkout(request):
    if not hasattr(request.user, 'cart'):
        return redirect('/profile/cart/')

    cart = request.user.cart
    items = cart.cartitem_set.all

    if cart.cartitem_set.count() < 1:
        return redirect('/profile/cart/')

    return render(request, 'shop/checkout.html', {
        'cart': cart,
        'items': items
    })


@login_required()
def checkout_confirm(request):
    if not hasattr(request.user, 'cart'):
        return redirect('/profile/cart/')

    cart = request.user.cart
    items = cart.cartitem_set.all

    new_order = Order(user=request.user)
    new_order.save()

    cart_count = cart.cartitem_set.count()

    # THIS PIECE OF SHIT CODE DOES NOT WORK RIGHT NOW
    for x in range(1, cart_count):
        order_product = OrderProduct(product=cart.cartitem_set.filter()[:x].get().product, order=new_order,
                                     quantity=cart.cartitem_set.filter()[:x].get().quantity)
        order_product.save()

    cart.delete()

    return HttpResponseRedirect(reverse('profile_orders'))
