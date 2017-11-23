from django.contrib import admin

from .models import Category, Comment, Grading, Product, Cart, CartItem

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Grading)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)