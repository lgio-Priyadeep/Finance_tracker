# test/test_api.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class TransactionAPITest(APITestCase):
    def test_create_transaction(self):
        url = reverse('create_transaction')
        data = {
            "user_id": 1,
            "amount": "100.00",
            "date": "2025-03-17",
            "description": "Test Transaction",
            "category": "Food",
            "type": "expense",
            "source": "cash"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("transaction_id", response.data)
