# pet-project-employee-salary-predict
"Pet" Django-Docker project with Unit tests for predicting salary.

RU

Для данного "pet" проекта был найден случайный набор данных
https://data.world/baltimore/6xv6-e66h/workspace/file?filename=baltimore-city-employee-salaries-fy2019-1.csv

Цель данного проекта: предсказать зарплату сотрудников в городе Балтимор.
Данные представлены за 2019 год.

Чтобы преступить к ознакомлению необходимо:

0. Стянуть проект
1. Ознакомиться с исследованием в файле salary-predict-research.ipynb (любые комментарии приветствуются)
2. Выполнить ноутбук salary-predict.ipynb
3. Развернуть Django проект
*  `docker-compose up`
4. Создать таблицы в базе данных
*  `python manage.py sqlmigrate employees 0001`
*  `python manage.py migrate`
5. Далее на главной странице http://0.0.0.0:8000 вам будет предложено мигрировать необходимые данные из .csv в таблицы базы данных
6. После чего можно будет выполнить предсказание.
7. При желании, можно создать администратора и просмотреть данные, которые используются в приложении
*  `python manage.py createsuperuser`
8. Так же, при желании можете прогнать юнит-тесты
*  `python manage.py test employees`


EN

A random dataset was found for this "pet" project
https://data.world/baltimore/6xv6-e66h/workspace/file?filename=baltimore-city-employee-salaries-fy2019-1.csv

Purpose of this project: to predict the salary of employees in the city of Baltimore.
Data are presented for 2019.

To proceed to acquaintance, you need:

0. Pull the project
1. Read my research in the salary-predict-research.ipynb file (you are more than welcome to leave any comments)
2. Run the notebook salary-predict.ipynb
3. Deploy the Django project 
  * `docker-compose up`
4. Create tables in the database
  * `python manage.py sqlmigrate employees 0001`
  * `python manage.py migrate`
5. Further on the main page http://0.0.0.0:8000 you will be prompted to migrate the necessary data from .csv to the database tables
6. After that it will be possible to perform the prediction.
7. Optionally, you can create an administrator and view the data used in the application
  * `python manage.py createsuperuser`
8. Also, if you wish, you can run unit tests
  * `python manage.py test employees`
