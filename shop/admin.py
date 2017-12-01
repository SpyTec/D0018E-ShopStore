from django.contrib import admin

from .models import Category, Comment, Rating, Product, Cart, CartItem

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)