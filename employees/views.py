from django.db import DatabaseError
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, \
    HttpResponseServerError
import pandas as pd
import pickle
import os
from datetime import datetime

from .models import Employees, Department, JobTitle


def index(request):
    departments = Department.objects.all()
    jobtitles = JobTitle.objects.all()
    if len(departments) == 0 or len(jobtitles) == 0:
        return render(request, 'migrations.html')
    else:
        return render(request, 'predict.html', {'departments': departments})


def results(request):
    data = {"dataset": Employees.objects.order_by('-id')}
    return render(request, "results.html", data)


def get_jobtitles_by_dep_id(request, dep_id):
    try:
        dep = Department.objects.get(pk=dep_id)
    except Department.DoesNotExist:
        return HttpResponse('Exception: Department Not Found')
    else:
        return JsonResponse(list(dep.jobtitle_set.all().values()), safe=False)


def predict_salary(request):
    if request.POST.get('action') == 'post':
        # Receive data from client
        name = request.POST.get('name')
        department = request.POST.get('department')
        jobtitle = request.POST.get('jobtitle')
        annual_rt = float(request.POST.get('annual_rt'))
        hire_date = request.POST.get('hire_date')
        work_exp = convert_hire_date_to_work_exp(hire_date)

        department_le = convert_le(department, '/code/le_department.pickle')
        jobtitle_le = convert_le(jobtitle, '/code/le_jobtitle.pickle')

        final_data = pd.DataFrame(
            data={
                'jobtitle': jobtitle_le[0],
                'descr': department_le[0],
                'annual_rt': annual_rt,
                'work_exp': work_exp
            },
            index=[0]
        )

        model_file = '/code/salary-predict.pickle'
        prediction = get_prediction(final_data, model_file)

        Employees.objects.create(
            name=name,
            annual_rt=annual_rt,
            hire_date=hire_date,
            department_id=Department.objects.get(name=department).id,
            jobtitle_id=JobTitle.objects.get(name=jobtitle).id,
            gross=prediction
        )

        return JsonResponse({
            'result': prediction,
            'work_exp': work_exp,
            'department': department
        }, safe=False)


def convert_hire_date_to_work_exp(date):
    convert_point = datetime(2020, 1, 1)
    work_exp = convert_point - datetime.strptime(date, '%Y-%m-%d')
    return float(str(work_exp).split()[0])

def convert_le(entity, path):
    if not os.path.exists(path):
        raise FileNotFoundError('File for label encoding conversion not found, please perform salary-predict.ipynb first')

    le = pickle.load(open(path, "rb"))
    return list(le.transform([entity]))


def get_prediction(final_data, model_file_path):
    if not os.path.exists(model_file_path):
        raise FileNotFoundError('Model file not found, please perform salary-predict.ipynb first')

    model = pickle.load(open(model_file_path, "rb"))
    result = model.predict(final_data)
    return round(float(result[0]), 2)


def perform_migration(request):
    file_path = '/code/baltimore-city-employee-salaries-fy2019.csv'

    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        return HttpResponseNotFound('File not found at ' + file_path)
    else:
        if migrate_departments(data) == 'success' and migrate_jobtitles(data) == 'success':
            return JsonResponse({'message': 'success'}, safe=False)


def migrate_departments(data):
    uid = data['DEPTID'].str[:3]
    name = data['DESCR'].str.replace('(\s+[( ]$|\s+\(\d{3}\)$|\s+\(\d{1}$)', '', regex=True)

    df = pd.DataFrame(data={'uid': uid, 'name': name})
    df = df.drop_duplicates(subset=['uid']).sort_values(by=['name'])

    df_records = df.to_dict('records')

    model_instances = [Department(
        uid=record['uid'],
        name=record['name'],
    ) for record in df_records]

    try:
        Department.objects.bulk_create(model_instances)
    except DatabaseError as e:
        return HttpResponseServerError(
            'Exception: Error while migrating data into employees_department table \n' + str(e)
        )
    else:
        return 'success'


def migrate_jobtitles(data):
    if Department.objects.count() == 0:
        raise DatabaseError('employees_department table is empty')

    department_ids_mapping = dict(Department.objects.values_list('uid', 'id'))
    uid = data['DEPTID'].str[:3]
    jobtitle = data['JOBTITLE']

    df = pd.DataFrame(data={'uid': uid, 'jobtitle': jobtitle})
    df = df.drop_duplicates(subset=['jobtitle']).sort_values(by=['jobtitle'])

    df['department_id'] = df['uid'].replace(department_ids_mapping)

    df_records = df.to_dict('records')

    model_instances = [JobTitle(
        name=record['jobtitle'],
        department_id=record['department_id'],
    ) for record in df_records]

    try:
        JobTitle.objects.bulk_create(model_instances)
    except DatabaseError as e:
        return HttpResponseServerError(
            'Exception: Error while migrating data into employees_jobtitle table \n' + str(e)
        )
    else:
        return 'success'
