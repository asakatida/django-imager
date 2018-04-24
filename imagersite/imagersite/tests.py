from django.test import TestCase, Client


class ProfileUnitTests(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()

    def tearDown(self):
        self.client = None
        super().setUp()

    def test_get_home_page(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'generic/home.html')
        self.assertEqual(response.templates[1].name, 'generic/base.html')