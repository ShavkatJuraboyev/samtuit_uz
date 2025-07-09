from django import forms
from .models import GrantApplication

class GrantApplicationForm(forms.ModelForm):
    class Meta:
        model = GrantApplication
        fields = ['new_phone', 'file', 'social_activism_flied']
        widgets = {
            'new_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Yangi telefon raqam'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'social_activism_flied': forms.FileInput(attrs={'class': 'form-control'}),
        }
