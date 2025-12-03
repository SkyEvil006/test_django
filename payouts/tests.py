import pytest
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Payout
from unittest.mock import patch


class PayoutModelTest(TestCase):
    def test_payout_creation(self):
        payout = Payout.objects.create(
            amount=100.00,
            currency='USD',
            recipient_details={'account': '123456'}
        )
        self.assertEqual(payout.amount, 100.00)
        self.assertEqual(payout.currency, 'USD')
        self.assertEqual(payout.status, Payout.Status.PENDING)


class PayoutAPITest(APITestCase):
    def test_create_payout(self):
        data = {
            'amount': 50.00,
            'currency': 'EUR',
            'recipient_details': {'iban': 'DE123456789'},
            'description': 'Test payout'
        }
        with patch('payouts.views.process_payout.delay') as mock_task:
            response = self.client.post('/api/v1/payouts/', data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Payout.objects.count(), 1)
            mock_task.assert_called_once()

    def test_list_payouts(self):
        Payout.objects.create(amount=100.00, currency='USD', recipient_details={'account': '123'})
        response = self.client.get('/api/v1/payouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_payout_detail(self):
        payout = Payout.objects.create(amount=100.00, currency='USD', recipient_details={'account': '123'})
        response = self.client.get(f'/api/v1/payouts/{payout.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], '100.00')

    def test_update_payout_status(self):
        payout = Payout.objects.create(amount=100.00, currency='USD', recipient_details={'account': '123'})
        data = {'status': Payout.Status.COMPLETED}
        response = self.client.patch(f'/api/v1/payouts/{payout.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payout.refresh_from_db()
        self.assertEqual(payout.status, Payout.Status.COMPLETED)

    def test_delete_payout(self):
        payout = Payout.objects.create(amount=100.00, currency='USD', recipient_details={'account': '123'})
        response = self.client.delete(f'/api/v1/payouts/{payout.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

