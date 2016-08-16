"""Mortality URL Configuration

"""
from django.conf.urls import url
from django.conf import settings
from django.contrib import admin

from django.conf.urls.static import static

from website.views import IndexPage, InputForm, nnMortalityResult

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^$', IndexPage.as_view(), name="website_index"),
    
     url(r'^form/$', InputForm.as_view(), name="website_input_form"),
     url(r'^result/$', nnMortalityResult.as_view(), name="website_mortality_result"),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
