from django.db import models
from django_mysql.models import JSONField

# Create your models here.

#Model to store the search history
class Data(models.Model):
    start_point = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    search_date = models.DateField(auto_now=True)
    google_response = models.TextField(max_length=1000)
    weather_response = models.TextField(max_length=1000)


class DataTable(models.Model):
    Start = models.CharField(max_length=200)
    End = models.CharField(max_length=200)
    Mode = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)
    google_response = models.TextField(max_length=1000)
    weather_response = models.TextField(max_length=1000)


class ModelDataTable(models.Model):
    Start = models.CharField(max_length=200)
    End = models.CharField(max_length=200)
    Mode = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)
    google_response = JSONField()
    weather_response = models.TextField(max_length=1000)


class Model_DataTable(models.Model):
    Start = models.CharField(max_length=200)
    End = models.CharField(max_length=200)
    Mode = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)
    google_response = JSONField()
    weather_response = JSONField()