from django.contrib import admin

from .models import Category, CategoryProduct, Comment, Grading, Product

admin.site.register(Category)
admin.site.register(CategoryProduct)
admin.site.register(Comment)
admin.site.register(Grading)
admin.site.register(Product)
