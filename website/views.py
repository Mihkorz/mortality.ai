# -*- coding: utf-8 -*-
import os
import uuid
import pandas as pd
import numpy as np
import subprocess
import json

from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.conf import settings
from django.shortcuts import redirect
from django import forms
from django.utils.safestring import mark_safe
from django.core.files import File

from django_countries.fields import LazyTypedChoiceField, Country
from django_countries.widgets import CountrySelectWidget
from django_countries import countries

from core.algorythm import ages_left
from .models import RunnedTest, Article

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip 

class nnBloodForm(forms.Form):
    
    """ TOP 10 markers """
    
    Albumen = forms.FloatField( label=mark_safe("<a href='https://en.wikipedia.org/wiki/Serum_albumin' target='_blank'>Albumin**</a>"),
                                  required=True, help_text='35 - 52 g/l', widget=forms.NumberInput(attrs={'class': 'form-control'}), 
                                      min_value=1, max_value=52.25)#min_value=35, max_value=52)    
    Glucose = forms.FloatField( label=mark_safe("<a href='https://en.wikipedia.org/wiki/Glucose' target='_blank'>Glucose**</a>"),
                                  required=True, help_text='3.9 - 5.8 mmole/l', widget=forms.NumberInput(attrs={'class': 'form-control'}), 
                                      min_value=0.35, max_value=32)#min_value=3.9, max_value=5.8)
    Alkaline_phosphatase = forms.FloatField( label=mark_safe("<a href='https://en.wikipedia.org/wiki/Alkaline_phosphatase' target='_blank'>Alkaline phosphatase**</a>"),
                                               required=True, help_text='20 - 120 U/l', widget=forms.NumberInput(attrs={'class': 'form-control'}), 
                                      min_value=1, max_value=4337)#min_value=20, max_value=120)
    Urea = forms.FloatField( label=mark_safe("<a href='https://en.wikipedia.org/wiki/Urea' target='_blank'>Urea**(BUN)</a>"),
                               required=True, help_text='2.5 - 6.4 mmole/l', widget=forms.NumberInput(attrs={'class': 'form-control'}), 
                                      min_value=0.7, max_value=84.1)#min_value=2.5, max_value=6.4)
    Erythrocytes = forms.FloatField( label=mark_safe("<a href='https://en.wikipedia.org/wiki/Red_blood_cell' target='_blank'>Erythrocytes** (RBC)</a>"),
                                       required=True, help_text=mark_safe('3.5 - 5.5 10<sup><small>6</small></sup> /mcl'),  widget=forms.NumberInput(attrs={'class': 'form-control'}), 
                                      min_value=0.79, max_value=9.25)#min_value=3.5, max_value=5.5)
    Cholesterol = forms.FloatField( label=mark_safe("<a href='https://en.wikipedia.org/wiki/Cholesterol' target='_blank'>Cholesterol**</a>"),
                                      required=True, help_text='3.37 - 5.96 mmole/l', widget=forms.NumberInput(attrs={'class': 'form-control '}), 
                                      min_value=1, max_value=20.19)#min_value=3.37, max_value=5.96)
    RDW = forms.FloatField( label=mark_safe("<a href='https://en.wikipedia.org/wiki/Red_blood_cell_distribution_width' target='_blank'>RDW**</a>"),
                              required=True, help_text='11.5 - 14.5 %', widget=forms.NumberInput(attrs={'class': 'form-control'}), 
                                      min_value=1, max_value=44.2)#min_value=11.5, max_value=14.5)
    Alpha_1_globulins1 = forms.FloatField( label=mark_safe("<a href='https://en.wikipedia.org/wiki/Alpha_globulin' target='_blank'>Alpha-2-globulins**</a>"), 
                                            required=True, help_text='5.1 - 8.5 g/l', widget=forms.NumberInput(attrs={'class': 'form-control'}), 
                                      min_value=1, max_value=20.17)#min_value=5.1, max_value=8.5)
    Hematocrit = forms.FloatField( label=mark_safe("<a href='https://en.wikipedia.org/wiki/Hematocrit' target='_blank'>Hematocrit**</a>"), 
                                    required=True, help_text='37 - 50 %', widget=forms.NumberInput(attrs={'class': 'form-control'}), 
                                      min_value=8, max_value=66)#min_value=37, max_value=50)
    Lymphocytes = forms.FloatField( label=mark_safe("<a href='https://en.wikipedia.org/wiki/Lymphocyte' target='_blank'>Lymphocytes**</a>"),
                                      required=True, help_text='20 - 40 %', widget=forms.NumberInput(attrs={'class': 'form-control '}), 
                                      min_value=0, max_value=98)#min_value=20, max_value=40) 
    country = LazyTypedChoiceField(choices=countries)
    
    class Meta:
        widgets = {'country': CountrySelectWidget(attrs={'class': 'form-control '})}



class IndexPage(TemplateView):
    template_name = 'website/index.html'
    
    def dispatch(self, request, *args, **kwargs):
        return super(IndexPage, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
              
        context = super(IndexPage, self).get_context_data(**kwargs)
        
        
        context['start_page_text'] = Article.objects.get(idx='start_page_text')
        
        return context
    
    
class InputForm(FormView):
    template_name = 'website/input_form.html'
    form_class = nnBloodForm
    success_url = '/result/'
    metric = 'eu'
    
    def dispatch(self, request, *args, **kwargs):
        
        
              
        return super(InputForm, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(InputForm, self).get_context_data(**kwargs)
        
        context['how_its_done'] = Article.objects.get(idx='how_its_done')
        context['rules'] = Article.objects.get(idx='rules')
        context['desc'] = Article.objects.get(idx='desc')
        
        context['metric'] = self.metric        
        context['document'] = 'input_document'
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        
        try:
            ip = get_client_ip(self.request)
        except:
            ip = 'Undefined'
        
        age =  float(self.request.POST.get('age'))
        if not age:
            age=30
        sex = int(self.request.POST.get('sex', 1))
        height = float(self.request.POST.get('height', 177))
        if not height:
            height = 177
        weight = float(self.request.POST.get('weight', 70.8))
        if not weight:
            weight = 70.8
        
        bmi = format((weight/(height**2))*10000, '.2f')
        
        country = self.request.POST.get('country')
        objCountry = Country(country)
        country_name = str(objCountry.alpha3)
        
        smoke = int(self.request.POST.get('smoke', 1))
        alcohol = int(self.request.POST.get('alcohol', 1))
        activity = int(self.request.POST.get('activity', 1))
        
        social_status = int(self.request.POST.get('social_status', 1))
        mental = False #2 b implemented later
        
        
        """ Aging Form"""
        df = pd.DataFrame() # DF for the full test
        
        df.loc[:,'Alpha-amylase'] = pd.Series(form.cleaned_data.get('Alpha_amylase', '59.91') if form.cleaned_data.get('Alpha_amylase') else 59.91)
        df.loc[:,'ESR (by Westergren)'] = pd.Series(form.cleaned_data.get('ESR') if form.cleaned_data.get('ESR') else 11.19)
        df.loc[:,'Bilirubin total'] = pd.Series(form.cleaned_data.get('Bilirubin_total') if form.cleaned_data.get('Bilirubin_total') else 13.01)
        df.loc[:,'Bilirubin direct'] = pd.Series(form.cleaned_data.get('Bilirubin_direct') if form.cleaned_data.get('Bilirubin_direct') else 4.85)
        df.loc[:,'Gamma-GT'] = pd.Series(form.cleaned_data.get('Gamma_GT') if form.cleaned_data.get('Gamma_GT') else 38.77)
        df.loc[:,'Glucose'] = pd.Series(form.cleaned_data.get('Glucose') if form.cleaned_data.get('Glucose') else 5.57)
        df.loc[:,'Creatinine'] = pd.Series(form.cleaned_data.get('Creatinine') if form.cleaned_data.get('Creatinine') else 74.72)
        df.loc[:,'Lactate dehydrogenase'] = pd.Series(form.cleaned_data.get('Lactate_dehydrogenase') if form.cleaned_data.get('Lactate_dehydrogenase') else 186.43)
        df.loc[:,'Urea'] = pd.Series(form.cleaned_data.get('Urea') if form.cleaned_data.get('Urea') else 5.17)
        df.loc[:,'Protein total'] = pd.Series(form.cleaned_data.get('Protein_total') if form.cleaned_data.get('Protein_total') else 73.01)
        
        df.loc[:,'Alpha-1-globulins'] = pd.Series(form.cleaned_data.get('Alpha_1_globulins') if form.cleaned_data.get('Alpha_1_globulins') else 2.92)
        df.loc[:,'Alpha-1-globulins1'] = pd.Series(form.cleaned_data.get('Alpha_1_globulins1') if form.cleaned_data.get('Alpha_1_globulins1') else 7.06)
        df.loc[:,'Beta-globulins'] = pd.Series(form.cleaned_data.get('Beta_globulins') if form.cleaned_data.get('Beta_globulins') else 7.99)
        df.loc[:,'Gamma-globulins'] = pd.Series(form.cleaned_data.get('Gamma_globulins') if form.cleaned_data.get('Gamma_globulins') else 11.47)
        df.loc[:,'Triglycerides'] = pd.Series(form.cleaned_data.get('Triglycerides') if form.cleaned_data.get('Triglycerides') else 1.36)
        df.loc[:,'Cholesterol'] = pd.Series(form.cleaned_data.get('Cholesterol') if form.cleaned_data.get('Cholesterol') else 5.48)
        df.loc[:,'HDL Cholesterol'] = pd.Series(form.cleaned_data.get('HDL_Cholesterol') if form.cleaned_data.get('HDL_Cholesterol') else 1.37)
        df.loc[:,'LDL cholesterol (by Friedewald)'] = pd.Series(form.cleaned_data.get('LDL_cholesterol') if form.cleaned_data.get('LDL_cholesterol') else 3.47)
        df.loc[:,'Alkaline phosphatase'] = pd.Series(form.cleaned_data.get('Alkaline_phosphatase') if form.cleaned_data.get('Alkaline_phosphatase') else 85.96)
        df.loc[:,'Calcium'] = pd.Series(form.cleaned_data.get('Calcium') if form.cleaned_data.get('Calcium') else 2.41)
        
        df.loc[:,'Chlorine'] = pd.Series(form.cleaned_data.get('Chlorine') if form.cleaned_data.get('Chlorine') else 104.86)
        df.loc[:,'Potassium'] = pd.Series(form.cleaned_data.get('Potassium') if form.cleaned_data.get('Potassium') else 4.36)
        df.loc[:,'Sodium'] = pd.Series(form.cleaned_data.get('Sodium') if form.cleaned_data.get('Sodium') else 140.09)
        df.loc[:,'Iron'] = pd.Series(form.cleaned_data.get('Iron') if form.cleaned_data.get('Iron') else 17.37)
        df.loc[:,'Hemoglobin'] = pd.Series(form.cleaned_data.get('Hemoglobin') if form.cleaned_data.get('Hemoglobin') else 13.9)
        df.loc[:,'Hematocrit'] = pd.Series(form.cleaned_data.get('Hematocrit') if form.cleaned_data.get('Hematocrit') else 40.89)
        df.loc[:,'MCH'] = pd.Series(form.cleaned_data.get('MCH') if form.cleaned_data.get('MCH') else 29.51)
        df.loc[:,'MCHC'] = pd.Series(form.cleaned_data.get('MCHC') if form.cleaned_data.get('MCHC') else 34.20)
        df.loc[:,'MCV'] = pd.Series(form.cleaned_data.get('MCV') if form.cleaned_data.get('MCV') else 86.52)
        df.loc[:,'Platelets'] = pd.Series(form.cleaned_data.get('Platelets') if form.cleaned_data.get('Platelets') else 259.77)
        
        df.loc[:,'Erythrocytes'] = pd.Series(form.cleaned_data.get('Erythrocytes') if form.cleaned_data.get('Erythrocytes') else 4.75)
        df.loc[:,'Leukocytes'] = pd.Series(form.cleaned_data.get('Leukocytes') if form.cleaned_data.get('Leukocytes') else 6.88)
        df.loc[:,'ALT'] = pd.Series(form.cleaned_data.get('ALT') if form.cleaned_data.get('ALT') else 27.58)
        df.loc[:,'AST'] = pd.Series(form.cleaned_data.get('AST') if form.cleaned_data.get('AST') else 24.96)
        df.loc[:,'Albumen'] = pd.Series(form.cleaned_data.get('Albumen') if form.cleaned_data.get('Albumen') else 43.57)
        df.loc[:,'Basophils, %'] = pd.Series(form.cleaned_data.get('Basophils') if form.cleaned_data.get('Basophils') else 0.32)
        df.loc[:,'Eosinophils, %'] = pd.Series(form.cleaned_data.get('Eosinophils') if form.cleaned_data.get('Eosinophils') else 2.93)
        df.loc[:,'Lymphocytes, %'] = pd.Series(form.cleaned_data.get('Lymphocytes') if form.cleaned_data.get('Lymphocytes') else 35.48)
        df.loc[:,'Monocytes, %'] = pd.Series(form.cleaned_data.get('Monocytes') if form.cleaned_data.get('Monocytes') else 8.79)
        df.loc[:,'NEUT'] = pd.Series(form.cleaned_data.get('NEUT') if form.cleaned_data.get('NEUT') else 55.10)
        df.loc[:,'RDW'] = pd.Series(form.cleaned_data.get('RDW') if form.cleaned_data.get('RDW') else 13.71)
        
        
        df.rename(columns={'Alpha-1-globulins1': 'Alpha-1-globulins'}, inplace=True)
        
        random_file_name = "%s.%s" % (uuid.uuid4(), 'csv')
        
        df.to_csv(settings.MEDIA_ROOT+"/uploads/"+random_file_name, index=False)
        
        upload =  open(settings.MEDIA_ROOT+"/uploads/"+random_file_name)
        
        try:
            command = "python django_call_age.py ../../media/uploads/"+random_file_name
            pipe = subprocess.Popen(command.split(), 
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                cwd=settings.MEDIA_ROOT+"/../static/nnblood/")
            stdout_data, stderr_data = pipe.communicate()
               
            if pipe.returncode != 0:
                raise RuntimeError("%r failed, status code %s stdout %r stderr %r" % (
                        command, pipe.returncode, stdout_data, stderr_data))
            result = stdout_data
        
            arResult = result.split('\n')
            predicted_age = arResult[0]
            
            median_age = np.median([float(predicted_age), float(age)])
        except:
            predicted_age = 0
            median_age = age
            
            #raise
        
            
        
        kwargs = {"gender": sex,       #0 = female, 1 = male 
          "country": country_name,      #country names as in 2 column of cntr.txt. For example France, Nigeria (case not sensitive)
          "age":median_age,                 #integer or float 0 - 999
          "height":height/100.0,            #float height in meters
          "weight":weight,              #float weight in kilograms
          "alcohol":alcohol,              #integer. Different meaning of value for men and women: 
                                    #For men  0 = non-drinker, 1 = < 1 drink/month, 2 = 0-4/week, 3 = 5-9/week, 4 = 10-24/week, 5 = binger 
                                    #For women  0 = non-drinker, 1 = < 1 drink/month, 2 = 0-2/week, 3 = 3-5/week, 4 = 6-17/week, 5 = binger
          "smoking":smoke,              #integer 0 = never smoked, 1 = formaer smoker, 2 = current light smoker, 3 = current heavy smoker
          "activity":activity,             #integer 0 = low activity, 1 = moderate, 2 = high
          "social_status":social_status,     #boolean. True = good social life, False = poor social life
          "mental":mental}           #boolean. True = active mental illnes, False = no active mental illness
        
        
        expected_longevity = ages_left(**kwargs)
        
        os.remove(settings.MEDIA_ROOT+"/uploads/"+random_file_name) #remove duplicate file
    
        #saving to DB    
        new_test = RunnedTest(ip = ip,
                              age = age,
                              sex = sex,
                              weight = weight,
                              height = height,
                              bmi = bmi,
                              smoking = smoke,
                              alcohol = alcohol,
                              ethnicity = objCountry,
                              social_status = social_status,
                              activity = activity,
                              mental_health = mental,
                              input_file = File(upload),
                              predicted_age = predicted_age,
                              
                              expected_longevity = expected_longevity)
        
        new_test.save()
    
        self.request.session['test_id'] = new_test.id
        
        #raise Exception('form')
        
        self.request.session['test_id'] = new_test.id
        return redirect(self.get_success_url())
    
        
    def form_invalid(self, form):
            return self.render_to_response(self.get_context_data(form=form))
    
    
class nnMortalityResult(TemplateView):
    template_name = 'website/nn_mortality_result.html'    
    
    
    
    def dispatch(self, request, *args, **kwargs):
        return super(nnMortalityResult, self).dispatch(request, *args, **kwargs)
        
    
    def get_context_data(self, **kwargs):
        context = super(nnMortalityResult, self).get_context_data(**kwargs)
        try:
            objTest = RunnedTest.objects.get(id=int(self.request.session['test_id']))
            context['test_id'] = objTest.id
            context['expected_longevity'] = objTest.expected_longevity
            
        except:
            context['expected_longevity'] = 'Undefined'
            

        return context      
    
    
    
    
    
    
    
    
    
    
    