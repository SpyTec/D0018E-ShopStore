from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    not_for_sale = models.BooleanField()


class CategoryProducts(models.Model):
    category = models.ForeignKey(Category)
    product = models.ForeignKey(Product)


class Grading(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    grading = models.BooleanField()


class Comment(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    comment = models.TextField()
