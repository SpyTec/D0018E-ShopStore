from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import generic
from shop.models import Product, Category, CartItem, Cart
from order.models import Order, OrderProduct
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError


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
    items = cart.cartitem_set.all()

    with transaction.atomic():
        try:
            # Check if sufficient inventory for whole order, else raise error before creating order
            for item in items:
                p = Product.objects.get(name=item.product.name)
                if item.quantity > p.inventory:
                    raise IntegrityError

            new_order = Order(user=request.user)
            new_order.save()

            for item in items:
                p = Product.objects.get(name=item.product.name)
                order_product = OrderProduct(product=item.product, order=new_order, quantity=item.quantity)
                order_product.save()
                p.inventory = p.inventory - item.quantity
                p.save()
            cart.delete()
        except IntegrityError:
            messages.warning(request, "Transaction failed, not enough in inventory!")
            return HttpResponseRedirect(reverse('profile_cart'))

        return HttpResponseRedirect(reverse('profile_orderdetail', args=(new_order.pk,)))
