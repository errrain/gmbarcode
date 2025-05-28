from django.urls import path
from .views import program_list, delete_program

urlpatterns = [
    path('', program_list, name='program_list'),
    path('delete/<int:pk>/', delete_program, name='delete_program'),
]
