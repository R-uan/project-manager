from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from .models import User

# Create your tests here.

class AccountTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_account(self):
        payload = {
            'email': 'me@gmail.com',
            'username': 'test_user',
            'first_name': 'me',
            'last_name': 'moi',
            'password': 'secret',
        }

        response = self.client.post(reverse('account_management'), payload)
        self.assertEqual(response.status_code, 200)

    def test_create_account_bad_request_email(self):
        payload = {
            # 'email': 'me@gmail.com',
            'username': 'test_user',
            'first_name': 'me',
            'last_name': 'moi',
            'password': 'secret',
        }

        response = self.client.post(reverse('account_management'), payload)
        self.assertEqual(response.status_code, 400)

    def test_create_account_bad_request_username(self):
        payload = {
            'email': 'me@gmail.com',
            # 'username': 'test_user',
            'first_name': 'me',
            'last_name': 'moi',
            'password': 'secret',
        }

        response = self.client.post(reverse('account_management'), payload)
        self.assertEqual(response.status_code, 400)

    def test_create_account_bad_request_password(self):
        payload = {
            'email': 'me@gmail.com',
            'username': 'test_user',
            'first_name': 'me',
            'last_name': 'moi',
            # 'password': 'secret',
        }

        response = self.client.post(reverse('account_management'), payload)
        self.assertEqual(response.status_code, 400)
