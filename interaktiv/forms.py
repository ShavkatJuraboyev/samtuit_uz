from django import forms
from .models import GrantApplication

class GrantApplicationForm(forms.ModelForm):
    class Meta:
        model = GrantApplication
        fields = ['new_phone', 'file']
        widgets = {
            'new_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Yangi telefon raqam'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
