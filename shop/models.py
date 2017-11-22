from profile.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


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
        return "User {} grade {}".format(self.user.username, self.grading)


class Comment(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    comment = models.TextField()

    def __str__(self):
        return self.comment


class Cart(models.Model):
    user = models.ForeignKey(User)

    def __str__(self):
        return "User {}".format(self.user.pk)


class ProductSnapshot(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    price_snapshot = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{}, price: {}".format(self.product.name, self.price_snapshot)
