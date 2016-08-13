from __future__ import unicode_literals

from django.db import models

from django_countries.fields import CountryField


class RunnedTest(models.Model):
    
    ip = models.CharField(max_length=30, blank=True)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    input_file = models.FileField("Blood markers file", upload_to='uploads/', blank=True)
    
    age = models.FloatField("Age", default='0', blank=True)
    sex = models.CharField("Sex", default='M', max_length=1, blank=True)
    weight = models.FloatField("Weight", default='0', blank=True)
    height = models.FloatField("Height", default='0', blank=True)
    bmi = models.FloatField("BMI", default='0', blank=True)
    smoking = models.CharField("Smoking", default='No', max_length=4,  blank=True)
    ethnicity = CountryField()
    social_status = models.CharField("Social status", default='', max_length=100,  blank=True)
    
    predicted_age = models.FloatField("Predicted age", default='0', blank=True)
    
