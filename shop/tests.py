from django.test import TestCase, Client
from .models import Category, Product


class RootTests(TestCase):
    def test_shop_root(self):
        client = Client()
        response = client.get('/shop')
        self.assertEqual(response.status_code, 301)

    def test_shop_root_(self):
        client = Client()
        response = client.get('/shop/')
        self.assertEqual(response.status_code, 200)

    def test_category_root(self):
        client = Client()
        response = client.get('/shop/category')
        # Maybe we should ad an redirect on this path to '/shop/category/'
        self.assertEqual(response.status_code, 301)

    def test_category_root_(self):
        client = Client()
        response = client.get('/shop/category/')
        # I think we should make this page
        self.assertEqual(response.status_code, 200)

    def test_category(self):
        client = Client()
        response = client.get('/shop/category/1')
        self.assertEqual(response.status_code, 301)

    def test_category_(self):
        category = Category(name='CPU')
        category.save()
        client = Client()
        response = client.get('/shop/category/1/')
        self.assertEqual(response.status_code, 200)

    def test_category_nonExistingCategory(self):
        client = Client()
        response = client.get('/shop/category/non/')
        self.assertEqual(response.status_code, 404)

    def test_product_root(self):
        client = Client()
        response = client.get('/shop/product')
        self.assertEqual(response.status_code, 404)

    def test_product_root_(self):
        client = Client()
        response = client.get('/shop/product/')
        self.assertEqual(response.status_code, 404)

    def test_product(self):
        client = Client()
        response = client.get('/shop/product/1')
        self.assertEqual(response.status_code, 301)

    def test_product_(self):
        product = Product(name='i7', description="Bla bla bla", price=200)
        product.save()
        client = Client()
        response = client.get('/shop/product/1/')
        self.assertEqual(response.status_code, 200)