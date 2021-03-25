from django.test import TestCase
from django.urls import reverse

from ..models import Department, JobTitle


class IndexTestCase(TestCase):

    def test_index_migration_page(self):
        """
        If migration was not done yet,
        tables are empty, we should see migration page
        """
        response = self.client.get(reverse('employees:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'migrations.html')
        self.assertContains(response, 'Hello and welcome!')

    def test_index_migration_page_department(self):
        """
        If employees_department table is not empty,
        but employees_jobtitle is empty, we should see migration page
        """
        Department.objects.create(uid='A99', name='Police Department')
        response = self.client.get(reverse('employees:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'migrations.html')
        self.assertContains(response, 'Hello and welcome!')

    def test_index_migration_page_jobtitle(self):
        """
        If  employees_jobtitle table is not empty,
        but employees_department is empty, we should see migration page
        """
        JobTitle.objects.create(name='Police Officer')
        response = self.client.get(reverse('employees:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'migrations.html')
        self.assertContains(response, 'Hello and welcome!')

    def test_index_predict_page(self):
        """
        If  employees_jobtitle table is not empty,
        and employees_department is not empty, we should see predict page
        """
        department = Department.objects.create(uid='A99', name='Police Department')
        JobTitle.objects.create(name='Police Officer', department_id=department.id)

        response = self.client.get(reverse('employees:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'predict.html')
        self.assertContains(response, 'Prediction Results')
