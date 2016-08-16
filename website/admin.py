from django.contrib import admin

from .models import RunnedTest

class RunnedTestAdmin(admin.ModelAdmin):
    list_display = ('id', 
                    'ip',
                    'datetime',
                    'age',
                    'predicted_age',
                    'sex',
                    'height',
                    'weight',
                    'bmi',
                    'smoking',
                    'alcohol',
                    'ethnicity',
                    'social_status',
                    'activity',
                    'mental_health',
                    'expected_longevity')

admin.site.register(RunnedTest, RunnedTestAdmin)