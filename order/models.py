from django.utils import timezone

from profile.models import User
from django.db import models
from django.db.models import Sum, F

from shop.models import Product


class Order(models.Model):

    STATUS = (
        ("0", 'Verified'),
        ("1", 'Shipped'),
        ("2", 'Received'),
        ("3", 'Refunded'),
    )

    ordered = models.DateTimeField(default=timezone.now)
    order_status = models.CharField(max_length=1, choices=STATUS, default='0')
    user = models.ForeignKey(User)

    @property
    def items(self):
        return self.orderproduct_set.aggregate(order_cost=Sum(
            F('cost') *
            F('quantity'),
            output_field=models.PositiveIntegerField()
        ))

    def __str__(self):
        return "Order: " + str(self.pk)


class OrderProduct(models.Model):
    quantity = models.IntegerField()
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    cost = models.IntegerField()

    def __str__(self):
        return "Order id: {}, Product id: {}, Quantity: {}".format(self.order.pk, self.product.pk, self.quantity)
