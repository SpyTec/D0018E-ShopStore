from django.test import TestCase, Client
from .models import Category, Product


class RootTests(TestCase):
    def test_shop_root_redirects(self):
        client = Client()
        response = client.get('/shop')
        self.assertEqual(response.status_code, 301)

    def test_shop_root_shows(self):
        client = Client()
        response = client.get('/shop/')
        self.assertEqual(response.status_code, 200)

    def test_category_root_redirects(self):
        client = Client()
        response = client.get('/shop/category')
        # Maybe we should ad an redirect on this path to '/shop/category/'
        self.assertEqual(response.status_code, 301)

    def test_category_root_shows(self):
        client = Client()
        response = client.get('/shop/category/')
        # I think we should make this page
        self.assertEqual(response.status_code, 200)

    def test_category_redirects(self):
        client = Client()
        response = client.get('/shop/category/1')
        self.assertEqual(response.status_code, 301)

    def test_category_displays_specific_category(self):
        product = Product(name='i7', description="Bla bla bla", price=200, inventory=3)
        product.save()
        product.categories.create(name='CPU')
        client = Client()
        response = client.get('/shop/category/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "i7")

    def test_category_nonExistingCategory(self):
        client = Client()
        response = client.get('/shop/category/non/')
        self.assertEqual(response.status_code, 404)

    def test_product_root_page_redirects(self):
        client = Client()
        response = client.get('/shop/product')
        self.assertEqual(response.status_code, 404)

    def test_product_root_page(self):
        client = Client()
        response = client.get('/shop/product/')
        self.assertEqual(response.status_code, 404)

    def test_product_page_redirects(self):
        client = Client()
        response = client.get('/shop/product/1')
        self.assertEqual(response.status_code, 301)

    def test_product_is_being_shown(self):
        product = Product(name='i7', description="Bla bla bla", price=200, inventory=3)
        product.save()
        client = Client()
        response = client.get('/shop/product/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bla bla bla")
