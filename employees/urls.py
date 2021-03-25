from django.urls import path
from . import views

app_name = "employees"

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('migrate/', views.perform_migration, name='perform_migration'),
    path('predict/', views.predict_salary, name='submit_prediction'),
    path('jobtitles/<int:dep_id>', views.get_jobtitles_by_dep_id, name='jobtitles'),
]
