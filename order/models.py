from profile.models import User
from django.db import models

from shop.models import Product


class Order(models.Model):

    STATUS = (
        ('A', 'Verified'),
        ('B', 'Shipped'),
        ('C', 'Received'),
    )

    order_status = models.CharField(max_length=1, choices=STATUS, default='A')
    user = models.ForeignKey(User)

    def __str__(self):
        return "Order: " + str(self.pk)


class OrderProduct(models.Model):
    quantity = models.IntegerField()
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)

    def __str__(self):
        return "Order id: {}, Product id: {}, Quantity: ".format(self.order.pk, self.product.pk, self.quantity)
