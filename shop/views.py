from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.views import generic

from shop.forms import CommentForm, SearchForm
from shop.models import Product, Category, CartItem, Cart, Rating, Comment
from order.models import Order, OrderProduct
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError


def product_view(request, pk):
    product = Product.objects.get(pk=pk)
    comments = Comment.objects.filter(product=product)

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid() :
            new_comment = Comment(user=request.user, product=product, comment=form.cleaned_data['comment'])
            new_comment.save()
        else:
            form = CommentForm()

    product_rating = None
    if request.user.is_authenticated():
        product_rating = product.rating_set.filter(product=product, user=request.user)
        if product_rating.count() == 0:
            product_rating = None
        else:
            product_rating = product_rating.first()

    ratings = product.rating_set
    positive_rating_percentage = None
    all_ratings = ratings.all().count()

    if all_ratings > 0:
        positive_ratings = ratings.filter(rating=True).count()

        if positive_ratings == 0:
            positive_rating_percentage = 0
        else:
            positive_rating_percentage = (positive_ratings / all_ratings) * 100

    return render(request, 'shop/detail.html', {
        'product': product,
        'product_rating': product_rating,
        'positive_rating_percentage': positive_rating_percentage,
        'comments': comments
    })


@login_required()
def rate_product(request, pk, rating):
    product = Product.objects.get(pk=pk)

    try:
        orders = Order.objects.filter(user=request.user)
    except ObjectDoesNotExist:
        messages.warning(request, "You need to buy the product first")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    has_bought_item = False
    for order in orders:
        order_items = order.orderproduct_set.filter(product=product)
        if order_items.count() > 0:
            has_bought_item = True
            break

    if not has_bought_item:
        messages.warning(request, "You need to buy the product first")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    Rating.objects.update_or_create(user=request.user, product=product, defaults={'rating': rating})

    messages.info(request, "Your rating has been registered!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class Overview(generic.ListView):
    template_name = 'shop/list.html'
    paginate_by = 25
    model = Product


class CategoryView(generic.ListView):
    model = Product
    template_name = 'shop/list_category.html'
    paginate_by = 25

    def get_queryset(self):
        pk = int(self.kwargs['pk'])
        return Product.objects.filter(categories__product=pk)


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
                order_product = OrderProduct(product=item.product, order=new_order, quantity=item.quantity,
                                             cost=item.product.price)
                order_product.save()
                p.inventory = p.inventory - item.quantity
                p.save()
            cart.delete()
        except IntegrityError:
            messages.warning(request, "Transaction failed, not enough in inventory!")
            return HttpResponseRedirect(reverse('profile_cart'))

        return HttpResponseRedirect(reverse('profile_orderdetail', args=(new_order.pk,)))


def search_view(request):
    # GET method
    if 'query' in request.GET:
        products_set = Product.objects.filter(name__contains=request.GET['query'])
        return render(request, 'shop/list.html', {
            'object_list': products_set
        })
    # POST method
    # if request.method == 'GET':
    #     search_form = SearchForm(request.GET)
    #     if search_form.is_valid():
    #         print("VALID")
    #         products_set = Product.objects.filter(name__contains=search_form.cleaned_data['query'])
    #         return render(request, 'shop/list.html', {
    #             'object_list': products_set
    #         })
    #     else:
    #         print("NOT valid")
    #         return None
    # return None