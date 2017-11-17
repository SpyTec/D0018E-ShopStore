from django.test import TestCase, Client


class HomeTestCase(TestCase):

    def test_home_has_shop_button(self):
        client = Client()
        response = client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Start shopping")
