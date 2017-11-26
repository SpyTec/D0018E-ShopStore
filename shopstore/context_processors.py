def category(request):
    from shop.models import Category
    categories = Category.objects.all()

    return {
        'categories': categories,
    }


def cart(request):
    if request.user.is_authenticated:
        cart_items = request.user.cart.cartitem_set

        from django.db.models import Sum
        return {
            'cart_items': cart_items.all(),
            'cart_item_count': cart_items.aggregate(Sum('quantity')).get('quantity__sum', 0.00),
        }
