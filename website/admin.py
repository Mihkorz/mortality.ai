from django.contrib import admin
from django.db import models


from pagedown.widgets import AdminPagedownWidget

from .models import RunnedTest, Article

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

class ArticleAdmin(admin.ModelAdmin):
    
    list_display =('idx',
                   'header',
                   'text')
    
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }

admin.site.register(RunnedTest, RunnedTestAdmin)
admin.site.register(Article, ArticleAdmin)