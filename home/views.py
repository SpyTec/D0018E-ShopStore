from django.shortcuts import render

# Create your views here.
from django.views import generic

from shop.models import Product


class IndexView(generic.ListView):
    template_name = 'home/index.html'
    model = Product
