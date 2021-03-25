from django.contrib import admin

from .models import Employees, Department, JobTitle


class JobTitleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'department']})
    ]
    list_display = ('name', 'department')
    search_fields = ['name']
    list_filter = ['name']


class DepartmentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['uid', 'name']})
    ]
    list_display = ('uid', 'name')
    search_fields = ['uid', 'name']
    list_filter = ['name']


class EmployeesAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'department', 'jobtitle', 'annual_rt', 'gross', 'hire_date']}),
    ]
    list_display = ('name', 'department', 'jobtitle', 'annual_rt', 'gross', 'hire_date')
    search_fields = ['name', 'department'],
    list_filter = ['department', 'jobtitle']

    class Media(object):
        js = (
            'js/jquery.min.js',  # app static folder
            'js/script.js',  # app static folder
        )


admin.site.register(Employees, EmployeesAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(JobTitle, JobTitleAdmin)
