from django.http import HttpResponseRedirect
from django.views import generic
from shop.models import Product, Category, ProductSnapshot, Cart
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
    product = Product.objects.get(pk=pk)
    ProductSnapshot(product=product, priceSnapshot=product.price).save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))