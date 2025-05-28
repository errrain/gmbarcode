from django import forms
from .models import ProductProgram

class ProductProgramForm(forms.ModelForm):
    class Meta:
        model = ProductProgram
        fields = ['name', 'description']
