from django import forms
from captcha.fields import CaptchaField
from samtuit.models import Contact
from interaktiv.models import ForeignStudent

class ContactForm(forms.ModelForm):
    captcha = CaptchaField()  # Captcha qo'shish
    
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'text']

class ForeignStudentForm(forms.ModelForm):  
    class Meta:
        model = ForeignStudent
        fields = ['first_name', 'last_name', 'phone', 'country', 'passport_file', 'diploma_file']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required':True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required':True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'required':True}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'passport_file': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'required':True}),
            'diploma_file': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'required':True}),
        }
