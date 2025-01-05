from rest_framework.test import APITestCase
import json
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .serializer import *
from rest_framework.test import APIClient

# Create your tests here.
class TestDetailCreditAnalysis(APITestCase):
    def setUp(self):
        # Create test data
        self.test_data1 = CreditAnalysis.objects.create(
            cust_id="123456",
            balance=1000.00,
            balance_freq=0.50,
            purch=500.00,
            onceoff_purch=200.00,
            install_purch=300.00,
            cash_adv=150.00,
            purch_freq=0.80,
            onceoff_purch_freq=0.30,
            purch_install_freq=0.50,
            cash_adv_freq=0.10,
            cash_adv_tRX=2,
            purch_tRX=3,
            cred_limit=5000.00,
            payments=450.00,
            min_payments=50.00,
            prc_full_payment=0.20,
            tenure=12,
        )

    def test_get_data_detail_url(self):
        url = reverse('data_detail', kwargs={'pk': self.test_data1.pk}) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_put_data_detail_url(self):
        url = (reverse('data_detail', kwargs={'pk': self.test_data1.pk}))
        updated_data = {"cust_id":123456, "balance": 1200.00}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.test_data1.refresh_from_db()
        self.assertEqual(self.test_data1.balance, 1200.00)
   
    def test_delete_data_detail_url(self):
        url = reverse('data_detail', kwargs={'pk': self.test_data1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(CreditAnalysis.objects.filter(pk=self.test_data1.pk).exists())

class TestCreditAnalysis(APITestCase):
    def test_create_data_url(self):
        url = reverse('create_data')
        response = self.client.post(url, {"cust_id": "123456",
        "balance": 1000.00,
        "balance_freq": 0.50,
        "purch": 500.00,
        "onceoff_purch": 200.00,
        "install_purch": 300.00,
        "cash_adv": 150.00,
        "purch_freq": 0.80,
        "onceoff_purch_freq": 0.30,
        "purch_install_freq": 0.50,
        "cash_adv_freq": 0.10,
        "cash_adv_tRX": 2,
        "purch_tRX": 3,
        "cred_limit": 5000.00,
        "payments": 450.00,
        "min_payments": 50.00,
        "prc_full_payment": 0.20,
        "tenure": 12,})
        self.assertEqual(response.status_code, 201)

    def test_filter_data_url(self):
        url = reverse('filter_data')
        response = self.client.get(url, {'balance': 1500, 'purch': 600})
        self.assertEqual(response.status_code, 200)

    def test_credit_analysis_url(self):
        url = reverse('credit_analysis_graphs')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

class TestAllFilterCreditAnalysis(APITestCase):
    def setUp(self):
        # Test data
        CreditAnalysis.objects.create(balance=1000, payments=500, min_payments=100, tenure=12)

        self.client = APIClient()

    def test_get_all_data_filter(self):
        url = reverse('get_all_data_filter')
        response = self.client.get(url, {'balance': 1000, 'payments': 500, 'min_payments': 100, 'tenure': 12})
        # response = self.client.get('/get_all_data_filter/?balance__gte=1500')

        filtered_data = CreditAnalysis.objects.filter(balance__gte=100, payments__lt=500, min_payments__lt=100, tenure__gt=12)
        serializer = CreditAnalysisSerializer(filtered_data, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(serializer.data))
