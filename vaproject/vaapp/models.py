from pyexpat import model
from typing import Tuple
from django.db import models

# Create your models here.

class Phsensor(models.Model):
    sensorName = models.CharField(max_length=8, blank=True)
    time = models.DateTimeField()
    value = models.FloatField()

    class Meta:
        db_table="ph"

class Temp(models.Model):
    sensorName = models.CharField(max_length=10, blank=True)
    time = models.DateTimeField()
    value = models.FloatField()

    class Meta:
        db_table="temperature"

class Batch(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    batch_id = models.CharField(blank=True, max_length=12)

    class Meta:
        db_table="batch"