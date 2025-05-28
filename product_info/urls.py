from django.urls import path
from . import views

urlpatterns = [
    path('select-program/', views.select_program, name='select_program'),
    path('list/<int:program_id>/', views.product_list, name='product_list'),
    path('create/<int:program_id>/', views.product_create, name='product_create'),
    path('detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('update/<int:pk>/', views.product_update, name='product_update'),  # ✅ 여기가 필요
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),
]
