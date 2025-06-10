# check_log_viewer/urls.py

from django.urls import path
from . import views

app_name = 'check_log_viewer'

urlpatterns = [
    path('', views.log_list, name='log_list'),
]