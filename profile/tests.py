from django.contrib.admin import ModelAdmin
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.models import Permission
from django.test import TestCase, Client
from django.urls import reverse

from order.models import Order
from profile.models import User
from shop.models import Product, Cart


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


class CartFunctionality(TestCase):
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

        self.product1 = Product.objects.create(
            name="Abc2",
            description="123",
            price=10,
            inventory=10,
            not_for_sale=0,
        )

        self.product2 = Product.objects.create(
            name="Abc1",
            description="456",
            price=3,
            inventory=5,
            not_for_sale=0,
        )

        self.cart = Cart.objects.create(
            user=self.user
        )

    def test_cart_is_empty(self):
        data = {
            'username': self.user.email,
            'password': self.password,
        }
        self.client.login(**data)

        response = self.client.get(reverse('profile_cart'))

        self.assertContains(response, "Cart is empty")

    def test_can_add_product_to_cart(self):
        data = {
            'username': self.user.email,
            'password': self.password,
        }
        self.client.login(**data)

        quantity = 5
        response = self.client.post(reverse('shop_add_to_cart', args=(self.product1.pk,)), {
            'quantity': quantity
        }, follow=True)

        self.assertContains(response, "{} has been added to cart".format(self.product1.name))

        cart_response = self.client.get(reverse('profile_cart'))

        self.assertContains(cart_response, self.product1.name)
        self.assertContains(cart_response, quantity * self.product1.price)

    def test_cart_has_update_and_buy_buttons(self):
        self.client.force_login(self.user)

        self.client.post(reverse('shop_add_to_cart', args=(self.product1.pk,)), {
            'quantity': 5
        })

        cart_response = self.client.get(reverse('profile_cart'))

        self.assertContains(cart_response, "Update cart")
        self.assertContains(cart_response, "Buy")

    def test_cart_total_cost_is_correct(self):
        self.client.force_login(self.user)

        quantity1 = 5
        self.client.post(reverse('shop_add_to_cart', args=(self.product1.pk,)), {
            'quantity': quantity1
        })

        quantity2 = 3
        self.client.post(reverse('shop_add_to_cart', args=(self.product2.pk,)), {
            'quantity': quantity2
        })

        cart_response = self.client.get(reverse('profile_cart'))

        self.assertContains(cart_response,
                            "{}&nbsp;kr".format(quantity1 * self.product1.price + quantity2 * self.product2.price))

    def test_cart_number_shows_correct_number(self):
        data = {
            'username': self.user.email,
            'password': self.password,
        }
        self.client.login(**data)

        quantity1 = 6
        self.client.post(reverse('shop_add_to_cart', args=(self.product1.pk,)), {
            'quantity': quantity1 - 1
        }, follow=True)
        self.client.post(reverse('shop_add_to_cart', args=(self.product1.pk,)), {
            'quantity': quantity1
        }, follow=True)

        quantity2 = 5
        response = self.client.post(reverse('shop_add_to_cart', args=(self.product2.pk,)), {
            'quantity': quantity2
        }, follow=True)

        self.assertContains(response, 'Cart <span class="badge badge-light">{}</span>'.format(quantity1 + quantity2))

    def test_can_increase_product_quantity_in_cart(self):
        self.client.force_login(self.user)

        quantity = 5
        self.client.post(reverse('shop_add_to_cart', args=(self.product1.pk,)), {
            'quantity': quantity
        }, follow=True)

        cart_response = self.client.get(reverse('profile_cart'))
        self.assertContains(cart_response, 'value="{}"'.format(quantity))
        quantity = quantity + 1
        post_parameters = {'cartitem_set-0-id': self.product1.pk,
                           'cartitem_set-0-quantity': quantity,
                           'cartitem_set-TOTAL_FORMS': 1,
                           'cartitem_set-INITIAL_FORMS': 1,
                           }

        cart_response = self.client.post(reverse('profile_cart'),
                                         data=post_parameters,
                                         follow=True,
                                         HTTP_REFERER=reverse('profile_cart'))
        self.assertContains(cart_response, 'Cart updated')
        self.assertContains(cart_response, 'value="{}"'.format(quantity))

    def test_can_decrease_product_quantity_in_cart(self):
        self.client.force_login(self.user)

        quantity = 6
        self.client.post(reverse('shop_add_to_cart', args=(self.product1.pk,)), {
            'quantity': quantity
        }, follow=True)

        cart_response = self.client.get(reverse('profile_cart'))
        self.assertContains(cart_response, 'value="{}"'.format(quantity))
        quantity = quantity - 1
        post_parameters = {'cartitem_set-0-id': self.product1.pk,
                           'cartitem_set-0-quantity': quantity,
                           'cartitem_set-TOTAL_FORMS': 1,
                           'cartitem_set-INITIAL_FORMS': 1,
                           }

        cart_response = self.client.post(reverse('profile_cart'),
                                         data=post_parameters,
                                         follow=True,
                                         HTTP_REFERER=reverse('profile_cart'))
        self.assertContains(cart_response, 'Cart updated')
        self.assertContains(cart_response, 'value="{}"'.format(quantity))

    def test_cart_does_not_show_when_logged_out(self):
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, 'Cart <span class="badge badge-light">')

    def test_can_visit_cart_without_products_added(self):
        user = User.objects.create(
            email="text@example.cam",
            first_name="John",
            last_name="Doe",
            personal_id="20171118-1235",
            address="Gatan 2",
            city="Luleå",
            zip_code="97434",
            phone_number="0731234567",
            is_staff=True,
        )
        password = 'Abcde123456'
        user.set_password(password)
        user.save()

        self.client.force_login(user)

        cart_response = self.client.get(reverse('profile_cart'))
        self.assertEquals(cart_response.status_code, 200)
