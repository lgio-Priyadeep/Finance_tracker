# test/test_api.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
class TransactionAPITest(APITestCase):
    def setUp(self):
    # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.token, _ = Token.objects.get_or_create(user=self.user)
        # Include the token in the request headers
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_transaction(self):
        url = reverse('create_transaction')
        data = {
            "user_id": 1,
            "amount": "100.00",
            "txn_date": "2025-03-17",
            "description": "Test Transaction",
            "category": "Food",
            "txn_type": "expense",
            "source": "cash"
        }
        response = self.client.post(url, data, format='json')
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("transaction_id", response.data)
