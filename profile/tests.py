from django.contrib.admin import ModelAdmin
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

        self.order = Order.objects.create(
            order_status='0',
            user=self.user,
        )

    def test_cannot_login_to_admin_panel(self):
        data = {
            'username': self.user.email,
            'password': self.password,
        }
        form = AdminAuthenticationForm(None, data)
        self.assertEquals(form.is_valid(), False)

    def test_display_as_logged_out_on_template(self):
        response = self.client.get(reverse('profile'))
        self.assertEquals(response.status_code, 302)
        pass

    def test_display_as_logged_in_on_template(self):
        data = {
            'username': self.user.email,
            'password': self.password,
        }
        is_logged_in = self.client.login(**data)
        self.assertEquals(is_logged_in, True)
        response = self.client.get(reverse('profile'))
        self.assertEquals(response.status_code, 200)

    def test_can_see_orders(self):
        data = {
            'username': self.user.email,
            'password': self.password,
        }
        is_logged_in = self.client.login(**data)
        self.assertEquals(is_logged_in, True)

        response = self.client.get(reverse('profile_orders'))
        self.assertContains(response, "Verified")


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
            order_status='0',
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

    # def test_can_edit_order_status(self):
    #     data = {
    #         'username': self.user.email,
    #         'password': self.password,
    #     }
    #     is_logged_in = self.client.login(**data)
    #     self.assertEquals(is_logged_in, True)
    #     ma = ModelAdmin(Order, self)
    #     ma_form = ma.form
    #     ma_form['order_status'] = '1'
    #     ma_form.save()
    #
    #     # order_data = {
    #     #     'order_status': '1',
    #     #     "user": self.user.id,
    #     #     "ordered_0": self.order.ordered,
    #     #     "ordered_1": self.order.ordered,
    #     # }
    #     # response = self.client.post('/admin/order/order/{}/change/'.format(self.order.id), order_data, follow=True)
    #     # print(response.content)
    #     self.assertEquals(Order.objects.get(id=self.order.id).order_status, '1')

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
