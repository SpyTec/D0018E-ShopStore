from profile.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField()
    inventory = models.PositiveIntegerField()
    not_for_sale = models.BooleanField(default=0)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Grading(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    grading = models.BooleanField()

    def __str__(self):
        return "User " + self.user.username + " grade " + self.grading


class Comment(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    comment = models.TextField()

    def __str__(self):
        return self.comment


class Cart(models.Model):
    user = models.ForeignKey(User)
    product = models.ManyToManyField(ProductSnapshot)

    def __str__(self):
        return "User: " + self.user.pk + ", has in basket: " + self.product


class ProductSnapshot(models.Model):
    product = models.ForeignKey(Product)
    price = models.PositiveIntegerField(default=product.price)  # Check if this changes over time or stays persistant

    def __str__(self):
        return self.product.name + ", price: " + str(self.price)
