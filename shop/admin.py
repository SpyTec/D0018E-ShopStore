from django.contrib import admin

from .models import Category, Comment, Grading, Product

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Grading)
admin.site.register(Product)
