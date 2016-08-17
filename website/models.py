from __future__ import unicode_literals

from django.db import models

from django_countries.fields import CountryField

SEX_TYPES = (
    (0, 'Female'),
     (1, 'Male'),             
)

SOCIAL_TYPES = (
    (0, 'Poor'),
     (1, 'Good'),             
)

MENTAL_TYPES = (
    (0, 'No active illness'),
     (1, 'Active illness'),             
)

SMOKING_TYPES = (
    (0, 'Never smoked'),
    (1, 'Former smoker'),
    (2, 'Current light smoker'),
    (3, 'Current heavy smoker'), 
)

ALCOHOL_MAN_TYPES = (
    (0, 'Non-drinker'),
    (1, '< 1 drink/month'),
    (2, '0-4/week'),
    (3, '5-9/week'), 
    (4, '10-24/week'),
    (5, 'Heavy drinker'),
)

ALCOHOL_WOMAN_TYPES = (
    (0, 'Non-drinker'),
    (1, '< 1 drink/month'),
    (2, '0-2/week'),
    (3, '3-5/week'), 
    (4, '6-17/week'),
    (5, 'Heavy drinker'),
)

ACTIVITY_TYPES = (
    (0, 'Low'),
    (1, 'Moderate'),
    (2, 'High'),    
)

class RunnedTest(models.Model):
    
    ip = models.CharField(max_length=30, blank=True)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    input_file = models.FileField("Blood markers file", blank=True)
    predicted_age = models.FloatField("Predicted age", default='0', blank=True)
    
    age = models.FloatField("Age", default=0, blank=True)
    sex = models.IntegerField("Sex", default=1, choices=SEX_TYPES, blank=True)
    weight = models.FloatField("Weight", default='0', blank=True)
    height = models.FloatField("Height", default='0', blank=True)
    bmi = models.FloatField("BMI", default='0', blank=True)
    smoking = models.IntegerField("Smoking", default=0, choices=SMOKING_TYPES, blank=True)
    alcohol = models.IntegerField("Alcohol", default=0,  choices=ALCOHOL_MAN_TYPES, blank=True)
    ethnicity = CountryField()
    social_status = models.IntegerField("Social status", default=1, choices=SOCIAL_TYPES,   blank=True)
    activity = models.IntegerField("Activity", default=0, choices=ACTIVITY_TYPES, blank=True)
    mental_health = models.IntegerField("Mental health", default=0, choices=MENTAL_TYPES, blank=True)
    
    expected_longevity = models.FloatField("Expected Longevity", default=0, blank=True)
    
class Article(models.Model):
    idx = models.CharField("Identificator", max_length=300, blank=False,
                           help_text = "Used to place text in the required container on page. Don't change")
    header = models.CharField("Header", max_length=300, blank=False,
                           help_text = "Text header")
    text = models.TextField(blank=False,)    
    
