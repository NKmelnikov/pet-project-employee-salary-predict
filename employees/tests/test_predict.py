from django.test import TestCase
from django.urls import reverse
import json
import pandas as pd
from ..views import migrate_departments, \
    migrate_jobtitles, \
    convert_hire_date_to_work_exp, \
    convert_le, \
    get_prediction

from ..models import Department,JobTitle



def migrate_departments_for_test(with_jobtitles=False):
    file_path = '/code/baltimore-city-employee-salaries-fy2019.csv'
    migrate_departments(pd.read_csv(file_path))

    if with_jobtitles:
        migrate_jobtitles(pd.read_csv(file_path))


class PredictTestCase(TestCase):

    def test_predict(self):
        """
        Test for submit_predict url
        """
        request_data = {
            'action': 'post',
            'name': 'Yuri Gagarin',
            'department': 'Mayors Office',
            'jobtitle': 'Executive Director V',
            'annual_rt': 100000,
            'hire_date': '1961-04-12',
        }

        migrate_departments_for_test()

        response = self.client.post(reverse('employees:submit_prediction'), data=request_data)
        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content['department'], 'Mayors Office')
        self.assertEqual(response_content['result'], 110137.83)

    def test_get_jobtitles_by_dep_id(self):
        """
        Test for get_jobtitles_by_dep_id function
        """
        Department.objects.create(id=1, uid='A99', name='Police Department')
        JobTitle.objects.create(name='Police Officer', department_id=1)

        response = self.client.get(reverse('employees:jobtitles', args=['1']))
        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content[0]['name'], 'Police Officer')
        self.assertEqual(len(response_content), 1)

    def test_convert_date(self):
        """
        Test for convert_hire_date_to_work_exp function
        """
        converted_date_1 = convert_hire_date_to_work_exp('2017-03-25')
        converted_date_2 = convert_hire_date_to_work_exp('1991-11-17')
        converted_date_3 = convert_hire_date_to_work_exp('2004-02-01')
        self.assertEqual(converted_date_1, 1012.0)
        self.assertEqual(converted_date_2, 10272.0)
        self.assertEqual(converted_date_3, 5813.0)

    def test_convert_le_not_found(self):
        """
        If file for label encoding conversion was not found
        we should see proper exception
        """
        fake_file_path = '/code/fake_le_department.pickle'
        with self.assertRaises(FileNotFoundError) as fnfe:
            convert_le('Mayors Office', fake_file_path)
        self.assertEqual(
            fnfe.exception.args[0],
            'File for label encoding conversion not found, please perform salary-predict.ipynb first'
        )

    def test_convert_le(self):
        """
        Test for convert_le function
        """
        file_path_department = '/code/le_department.pickle'
        file_path_jobtitle = '/code/le_jobtitle.pickle'
        self.assertEqual(convert_le('Mayors Office', file_path_department), [51])
        self.assertEqual(convert_le('Criminal Justice Associate', file_path_jobtitle), [244])

    def test_get_prediction_file_not_found(self):
        """
        If model file for prediction was not found
        we should see proper exception
        """
        fake_model_path = '/code/fake_salary-predict.pickle'
        with self.assertRaises(FileNotFoundError) as fnfe:
            get_prediction(pd.DataFrame(), fake_model_path)
        self.assertEqual(
            fnfe.exception.args[0],
            'Model file not found, please perform salary-predict.ipynb first'
        )

    def test_get_prediction(self):
        """
        Test for get_prediction function
        """
        data = {
            'jobtitle': 51,
            'descr': 244,
            'annual_rt': 100000.0,
            'work_exp': 492.0,
        }
        model_path = '/code/salary-predict.pickle'
        result = get_prediction(pd.DataFrame(data=data, index=[0]), model_path)
        self.assertEqual(result, 76107.91)
