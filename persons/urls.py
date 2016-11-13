# The views used below are normally mapped in django.contrib.admin.urls.py
# This URLs file is used to provide a reliable view deployment for test purposes.
# It is also provided as a convenience to those who want to deploy these URLs
# elsewhere.

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^persons/$', views.Persons.persons_list, name='persons_list_index'),
    url(r'^api/search_persons/$', views.Persons.json_search)
]