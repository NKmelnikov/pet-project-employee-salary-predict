from django.test import TestCase
from django.urls import reverse

from ..models import Employees


class ResultsTestCase(TestCase):

    def test_result_empty_page(self):
        """
        If migration was not done yet,
        tables are empty, we should see migration page
        """
        response = self.client.get(reverse('employees:results'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'results.html')
        self.assertContains(response, 'Here you`ll see employees with predicted salary')

    def test_result_not_empty_page(self):
        """
        If migration was done,
        tables are not empty, we should see results page
        """
        Employees.objects.create(name='Yuri Gagarin', annual_rt=1000000, gross=1000000, hire_date='1961-04-12')
        response = self.client.get(reverse('employees:results'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'results.html')
        self.assertContains(response, 'Yuri Gagarin')
