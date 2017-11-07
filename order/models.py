from django.contrib.auth.models import User
from django.db import models

from shop.models import Product


class Order(models.Model):

    STATUS = (
        (0, 'Verified'),
        (1, 'Shipped'),
        (2, 'Received'),
    )

    ordered = models.BooleanField()
    order_status = models.CharField(max_length=1, choices=STATUS)
    user = models.ForeignKey(User)

    def __str__(self):
        return "Ordered: " + self.pk


class OrderProduct(models.Model):
    quantity = models.IntegerField()
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)

    def __str__(self):
        return "(" + self.order.pk + ", " + self.product.pk + ")"
