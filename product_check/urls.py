from django.urls import path
from . import views

app_name = 'product_check'

urlpatterns = [
    path('products/<int:program_id>/', views.product_list, name='product_list'),
    path('barcode-check/<int:product_id>/', views.barcode_check, name='barcode_check'),
    path('save-error-log/', views.save_error_log, name='save_error_log'),
    path('save-success-log/', views.save_success_log, name='save_success_log'),
]
