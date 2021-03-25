from django.test import TestCase
from django.urls import reverse
from django.db import DatabaseError

import os
import pandas as pd
from ..views import migrate_departments, migrate_jobtitles

from ..models import Department, JobTitle


class MigrateTestCase(TestCase):
    file_path = '/code/baltimore-city-employee-salaries-fy2019.csv'


    def test_migrate(self):
        """
        If migration goes well,
        db should be filled up with data from csv file
        """
        response = self.client.get(reverse('employees:perform_migration'))

        assert os.path.exists(self.file_path) == 1

        assert Department.objects.count() == 56
        assert JobTitle.objects.count() == 1010

        assert Department.objects.filter(name='COMP-Audits').exists()
        assert Department.objects.filter(name='TRANS-Traffic').exists()

        assert JobTitle.objects.filter(name='911 Lead Operator').exists()
        assert JobTitle.objects.filter(name='Zoning Examiner I').exists()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'success')


    def test_migrate_departments(self):
        """
        Test for migrate_departments function
        """
        data = pd.read_csv(self.file_path)
        assert 'DEPTID' in data.columns
        assert 'DESCR' in data.columns
        assert len(data.index) == 13811

        response = migrate_departments(data)
        self.assertEqual(response, 'success')

    def test_migrate_jobtitles(self):
        """
        Test for migrate_jobtitles function
        """
        data = pd.read_csv(self.file_path)
        assert 'DEPTID' in data.columns
        assert 'JOBTITLE' in data.columns
        assert len(data.index) == 13811

        migrate_departments(data)
        response = migrate_jobtitles(data)
        self.assertEqual(response, 'success')

    def test_migrate_jobtitles_no_departments(self):
        """
        If migrate_departments has not been performed for some reason
        """
        data = pd.read_csv(self.file_path)

        with self.assertRaises(DatabaseError) as de:
            migrate_jobtitles(data)
        self.assertEqual(de.exception.args[0], 'employees_department table is empty')
