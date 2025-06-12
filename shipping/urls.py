# shipping/urls.py
from django.urls import path
from . import views

app_name = 'shipping'

urlpatterns = [
    path('', views.shipping_home, name='shipping_home'),
    path('start/', views.start_check, name='start_check'),
    path('scan/<int:session_id>/', views.scan_box, name='scan_box'),
    path('save-log/<int:session_id>/', views.save_shipping_log, name='save_shipping_log'),
    path('logs/', views.shipping_log_list, name='shipping_log_list'),
]