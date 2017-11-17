from django.shortcuts import render
from django.views import generic
from shop.models import Product, Category


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
