from django.shortcuts import render
from django.views import generic
from shop.models import Product


class IndexView(generic.ListView):
    template_name = 'shop/list.html'
    model = Product
