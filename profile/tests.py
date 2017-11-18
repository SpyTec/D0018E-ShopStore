from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.models import Permission
from django.test import TestCase, Client
from django.urls import reverse

from order.models import Order
from profile.models import User
from shop.models import Product


class Customer(TestCase):
    def setUp(self):
        self.user = User(
            email="text@example.com",
            first_name="John",
            last_name="Doe",
            personal_id="20171118-1234",
            address="Gatan 2",
            city="Luleå",
            zip_code="97434",
            phone_number="0731234567",
        )
        self.password = 'Abcde123456'
        self.user.set_password(self.password)
        self.user.save()

    def test_cannot_login_to_admin_panel(self):
        data = {
            'username': self.user.email,
            'password': self.password,
        }
        form = AdminAuthenticationForm(None, data)
        self.assertEquals(form.is_valid(), False)

    def test_display_as_logged_in_on_template(self):
        pass

    def test_display_as_logged_out_on_template(self):
        pass


class OrderHandlers(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="text@example.com",
            first_name="John",
            last_name="Doe",
            personal_id="20171118-1234",
            address="Gatan 2",
            city="Luleå",
            zip_code="97434",
            phone_number="0731234567",
            is_staff=True,
        )
        self.password = 'Abcde123456'
        self.user.set_password(self.password)
        self.user.save()
        self.user.user_permissions.add(Permission.objects.get(name="Can change order"))

        self.order = Order.objects.create(
            order_status='A',
            user=self.user,
        )

        self.product = Product.objects.create(
            name="Abc",
            description="Ddada",
            price=151,
            inventory=5,
            not_for_sale=0,
        )

    def test_can_login_to_admin_panel(self):
        data = {
            'username': self.user.email,
            'password': self.password,
        }
        form = AdminAuthenticationForm(None, data)
        self.assertEquals(form.is_valid(), True)
        pass

    def test_can_edit_order_status(self):
        data = {
            'username': self.user.email,
            'password': self.password,
        }
        is_logged_in = self.client.login(**data)
        self.assertEquals(is_logged_in, True)

        order_data = {
            'order_status': 'B',
            "user": self.user.id
        }
        self.client.post('/admin/order/order/{}/change/'.format(self.order.id), order_data, follow=True)

        self.assertEquals(Order.objects.get(id=1).order_status, 'B')

    def test_cannot_edit_order(self):
        # need to add specific permission to only change order status and not ordered
        pass

    def test_cannot_product(self):
        data = {
            'username': self.user.email,
            'password': self.password,
        }
        is_logged_in = self.client.login(**data)

        self.assertEquals(is_logged_in, True)
        response = self.client.get('/admin/shop/product/{}/change/'.format(self.product.id), follow=True)

        self.assertEquals(response.status_code, 403)
