from django.test import TestCase
from django.urls import reverse, NoReverseMatch

from order.models import Order, OrderProduct
from profile.models import User
from .models import Product, Cart, CartItem, Rating


class RatingTests(TestCase):
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

        self.product = Product.objects.create(name='i7', description="Bla bla bla", price=200, inventory=3)

    def test_rating_buttons_are_hidden_when_logged_out(self):
        response = self.client.get(reverse('shop_detail', args=(self.product.pk,)))
        self.assertNotContains(response, "Give your rating")

    def test_rating_buttons_are_visible_when_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('shop_detail', args=(self.product.pk,)))
        self.assertContains(response, "Give your rating")

    def test_ratings_are_visible_when_logged_out(self):
        Rating.objects.create(product=self.product, user=self.user, rating=1)
        response = self.client.get(reverse('shop_detail', args=(self.product.pk,)))
        self.assertContains(response, "Rating:")
        self.assertContains(response, '<div class="progress-bar bg-success" role="progressbar"')

    def test_ratings_are_visible_when_logged_in(self):
        Rating.objects.create(product=self.product, user=self.user, rating=1)
        self.client.force_login(self.user)
        response = self.client.get(reverse('shop_detail', args=(self.product.pk,)))
        self.assertContains(response, "Rating:")
        self.assertContains(response, '<div class="progress-bar bg-success" role="progressbar"')

    def test_user_can_add_good_rating(self):
        self.client.force_login(self.user)
        order = Order.objects.create(user=self.user)
        OrderProduct.objects.create(order=order, quantity=1, product=self.product, cost=5)
        _rating = 1
        response = self.client.post(reverse('product_rate', args=(self.product.pk, _rating,)), follow=True)
        ratingDb = Rating.objects.get(user=self.user, product=self.product, rating=_rating)
        self.assertContains(response, "Your rating has been registered")
        self.assertAlmostEqual(ratingDb.rating, _rating)

    def test_user_can_add_bad_rating(self):
        self.client.force_login(self.user)
        order = Order.objects.create(user=self.user)
        OrderProduct.objects.create(order=order, quantity=1, product=self.product, cost=5)
        _rating = 0
        response = self.client.post(reverse('product_rate', args=(self.product.pk, _rating,)), follow=True)
        ratingDb = Rating.objects.get(user=self.user, product=self.product, rating=_rating)
        self.assertContains(response, "Your rating has been registered")
        self.assertAlmostEqual(ratingDb.rating, _rating)

    def test_user_cannot_add_negative_rating(self):
        self.client.force_login(self.user)
        order = Order.objects.create(user=self.user)
        OrderProduct.objects.create(order=order, quantity=1, product=self.product, cost=5)
        _rating = -1
        got_exception = False
        try:
            self.client.post(reverse('product_rate', args=(self.product.pk, _rating,)), follow=True)
        except NoReverseMatch:
            got_exception = True

        ratingDb = Rating.objects.count()
        self.assertEqual(ratingDb, 0)
        self.assertEqual(got_exception, True)

    def test_user_can_change_rating(self):
        self.client.force_login(self.user)
        order = Order.objects.create(user=self.user)
        OrderProduct.objects.create(order=order, quantity=1, product=self.product, cost=5)
        _rating = 1
        Rating.objects.create(product=self.product, user=self.user, rating=(not _rating))
        response = self.client.get(reverse('shop_detail', args=(self.product.pk,)), follow=True)
        self.assertContains(response, '<a type="button" class="btn btn-danger"')

        response = self.client.post(reverse('product_rate', args=(self.product.pk, _rating,)), follow=True)
        ratingDb = Rating.objects.get(user=self.user, product=self.product, rating=_rating)
        self.assertContains(response, "Your rating has been registered")
        self.assertAlmostEqual(ratingDb.rating, _rating)


class CartTests(TestCase):
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

        self.cart = Cart.objects.create(
            user=self.user
        )

    def test_product_snapshot_defaults_to_zero(self):
        product = Product.objects.create(name='i7', description="Bla bla bla", price=200, inventory=3)
        ps = CartItem.objects.create(
            product=product,
            user_cart=self.cart,
        )
        self.assertEquals(ps.price_snapshot, 0)

    def test_cart_cascade_deletes(self):
        product = Product.objects.create(name='i7', description="Bla bla bla", price=200, inventory=3)
        ps = CartItem.objects.create(
            product=product,
            user_cart=Cart.objects.get(pk=self.cart.pk),
        )

        self.assertEquals(Cart.objects.filter(pk=self.cart.pk).count(), 1)
        self.assertEquals(CartItem.objects.filter(pk=ps.pk).count(), 1)

        Cart.objects.get(pk=self.cart.pk).delete()

        self.assertEquals(Cart.objects.filter(pk=self.cart.pk).count(), 0)
        self.assertEquals(CartItem.objects.filter(pk=ps.pk).count(), 0)


class RootTests(TestCase):
    def test_shop_root_redirects(self):
        response = self.client.get('/shop')
        self.assertEqual(response.status_code, 301)

    def test_shop_root_shows(self):
        response = self.client.get(reverse('shop'))
        self.assertEqual(response.status_code, 200)

    def test_category_root_redirects(self):
        response = self.client.get('/shop/category')
        self.assertEqual(response.status_code, 301)

    def test_category_root_shows(self):
        response = self.client.get('/shop/category/')
        self.assertEqual(response.status_code, 200)

    def test_category_redirects(self):
        response = self.client.get('/shop/category/1')
        self.assertEqual(response.status_code, 301)

    def test_category_displays_specific_category(self):
        product = Product(name='i7', description="Bla bla bla", price=200, inventory=3)
        product.save()
        product.categories.create(name='CPU')
        response = self.client.get(reverse('shop_category', args=(product.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "i7")

    def test_category_nonExistingCategory(self):
        response = self.client.get(reverse('shop_category', args=(0,)))
        self.assertEqual(response.status_code, 404)

    def test_product_root_page(self):
        response = self.client.get('/shop/product/')
        self.assertEqual(response.status_code, 404)

    def test_product_page_redirects(self):
        response = self.client.get('/shop/product/1')
        self.assertEqual(response.status_code, 301)

    def test_product_is_being_shown(self):
        product = Product(name='i7', description="Bla bla bla", price=200, inventory=3)
        product.save()
        response = self.client.get(reverse('shop_detail', args=(product.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bla bla bla")
