from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import generic
from shop.models import Product, Category, CartItem, Cart
from django.shortcuts import redirect, render
from django.forms import inlineformset_factory
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
        return redirect('/login/?next=%s' % request.path)

    cart = request.user.cart
    items = cart.cartitem_set
    return render(request, 'shop/checkout.html', {
        'cart': cart,
        'items': items
    })