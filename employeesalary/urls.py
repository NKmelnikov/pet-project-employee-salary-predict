from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('employees.urls', namespace='predict')),
    path('admin/', admin.site.urls),
]