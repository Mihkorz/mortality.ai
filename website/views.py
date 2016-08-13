
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.conf import settings
from django import forms
from django.utils.safestring import mark_safe

from django_countries.fields import LazyTypedChoiceField, Country
from django_countries.widgets import CountrySelectWidget
from django_countries import countries

class nnBloodForm(forms.Form):
    
    """ TOP 10 markers """
    
    Albumen = forms.FloatField( label=mark_safe("<a href='https://en.wikipedia.org/wiki/Serum_albumin' target='_blank'>Albumin**</a>"),
                                  required=False, help_text='35 - 52 g/l', widget=forms.NumberInput(attrs={'class': 'form-control'}), 
                                      min_value=1, max_value=52.25)#min_value=35, max_value=52)    
    Glucose = forms.FloatField( label=mark_safe("<a href='https://en.wikipedia.org/wiki/Glucose' target='_blank'>Glucose**</a>"),
                                  required=False, help_text='3.9 - 5.8 mmole/l', widget=forms.NumberInput(attrs={'class': 'form-control'}), 
                                      min_value=0.35, max_value=32)#min_value=3.9, max_value=5.8)
    Alkaline_phosphatase = forms.FloatField( label=mark_safe("<a href='https://en.wikipedia.org/wiki/Alkaline_phosphatase' target='_blank'>Alkaline phosphatase**</a>"),
                                               required=False, help_text='20 - 120 U/l', widget=forms.NumberInput(attrs={'class': 'form-control'}), 
                                      min_value=1, max_value=4337)#min_value=20, max_value=120)
    Urea = forms.FloatField( label=mark_safe("<a href='https://en.wikipedia.org/wiki/Urea' target='_blank'>Urea**(BUN)</a>"),
                               required=False, help_text='2.5 - 6.4 mmole/l', widget=forms.NumberInput(attrs={'class': 'form-control'}), 
                                      min_value=0.7, max_value=84.1)#min_value=2.5, max_value=6.4)
    Erythrocytes = forms.FloatField( label=mark_safe("<a href='https://en.wikipedia.org/wiki/Red_blood_cell' target='_blank'>Erythrocytes** (RBC)</a>"),
                                       required=False, help_text=mark_safe('3.5 - 5.5 10<sup><small>6</small></sup> /mcl'),  widget=forms.NumberInput(attrs={'class': 'form-control'}), 
                                      min_value=0.79, max_value=9.25)#min_value=3.5, max_value=5.5)
    Cholesterol = forms.FloatField( label=mark_safe("<a href='https://en.wikipedia.org/wiki/Cholesterol' target='_blank'>Cholesterol**</a>"),
                                      required=False, help_text='3.37 - 5.96 mmole/l', widget=forms.NumberInput(attrs={'class': 'form-control '}), 
                                      min_value=1, max_value=20.19)#min_value=3.37, max_value=5.96)
    RDW = forms.FloatField( label=mark_safe("<a href='https://en.wikipedia.org/wiki/Red_blood_cell_distribution_width' target='_blank'>RDW**</a>"),
                              required=False, help_text='11.5 - 14.5 %', widget=forms.NumberInput(attrs={'class': 'form-control'}), 
                                      min_value=1, max_value=44.2)#min_value=11.5, max_value=14.5)
    Alpha_1_globulins1 = forms.FloatField( label=mark_safe("<a href='https://en.wikipedia.org/wiki/Alpha_globulin' target='_blank'>Alpha-2-globulins**</a>"), 
                                            required=False, help_text='5.1 - 8.5 g/l', widget=forms.NumberInput(attrs={'class': 'form-control'}), 
                                      min_value=1, max_value=20.17)#min_value=5.1, max_value=8.5)
    Hematocrit = forms.FloatField( label=mark_safe("<a href='https://en.wikipedia.org/wiki/Hematocrit' target='_blank'>Hematocrit**</a>"), 
                                    required=False, help_text='37 - 50 %', widget=forms.NumberInput(attrs={'class': 'form-control'}), 
                                      min_value=8, max_value=66)#min_value=37, max_value=50)
    Lymphocytes = forms.FloatField( label=mark_safe("<a href='https://en.wikipedia.org/wiki/Lymphocyte' target='_blank'>Lymphocytes**</a>"),
                                      required=False, help_text='20 - 40 %', widget=forms.NumberInput(attrs={'class': 'form-control '}), 
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
        
        
        context['test'] = 'TEST VAR'
        
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
        
        
        context['metric'] = self.metric        
        context['document'] = 'input_document'
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
         
        height = self.request.POST['height']
        weight = self.request.POST['weight']
        smoke = self.request.POST['smoke']
        
        country = self.request.POST['country']
        
        aaa = Country(country)
        iso = aaa.alpha3
        
        raise Exception('form')
        pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    