from django.test import TestCase
from django.urls import reverse


class HomeTestCase(TestCase):

    def test_home_has_shop_button(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Start shopping")
