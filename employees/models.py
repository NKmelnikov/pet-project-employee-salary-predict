from django.db import models


class Department(models.Model):
    uid = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class JobTitle(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return self.name


class Employees(models.Model):
    name = models.CharField(max_length=255)
    hire_date = models.DateField(default=None, blank=True, null=True)
    annual_rt = models.IntegerField()
    gross = models.FloatField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=None, blank=True, null=True)
    jobtitle = models.ForeignKey(JobTitle, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return self.name
