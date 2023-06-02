import json
from django.test import TestCase
from django.urls import reverse


class ReportTestCase(TestCase):
    def test_generate_report(self):
        url = reverse('generate_report')
        valid_date = '2019-08-25'
        response = self.client.get(url, {'date': valid_date})
        self.assertEqual(response.status_code, 200)
        report = json.loads(response.content)
        self.assertIn('total_items_sold', report)
        self.assertIn('total_customers', report)
        self.assertIn('total_discount', report)
        self.assertIn('avg_discount_rate', report)
        self.assertIn('avg_order_total', report)
        self.assertIn('total_commissions', report)
        self.assertIn('avg_commissions_per_order', report)

    def test_generate_report_invalid_date(self):
        url = reverse('generate_report')
        invalid_date = '2023-99-99'
        response = self.client.get(url, {'date': invalid_date})
        self.assertEqual(response.status_code, 400)
        error = json.loads(response.content)
        self.assertEqual(error['error'], 'Invalid date')
