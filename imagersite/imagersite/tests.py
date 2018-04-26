"""Tests."""
from django.test import TestCase
from django.urls import reverse_lazy
from django.core import mail
from urllib.parse import urlparse


class ProfileUnitTests(TestCase):
    # def setUp(self):
    #     super().setUp()
    #     self.client = Client()

    # def tearDown(self):
    #     self.client = None
    #     super().setUp()

    def test_get_home_page(self):
        """ test home page """
        response = self.client.get(reverse_lazy('home'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'generic/home.html')
        self.assertEqual(response.templates[1].name, 'generic/base.html')

    def test_get_registration_page(self):
        """ test registration page """
        response = self.client.get(reverse_lazy('registration_register'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'registration/registration_form.html')
        self.assertEqual(response.templates[1].name, 'generic/base.html')

    def test_register_user(self):
        """ test for user registration """
        response = self.client.post(reverse_lazy('registration_register'), {'username': 'wat', 'password1': 'password', 'password2': 'password', 'email': 'wat@wat.com'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'registration/registration_complete.html')
        self.assertEqual(response.templates[1].name, 'generic/base.html')
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to, ['wat@wat.com'])
        register_url = email.body.splitlines()[-1]
        register_url = urlparse(register_url)
        response = self.client.get(register_url.path)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.login(username='wat', password='password'))
