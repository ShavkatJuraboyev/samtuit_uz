from django import forms
from captcha.fields import CaptchaField
from samtuit.models import Contact

class ContactForm(forms.ModelForm):
    captcha = CaptchaField()  # Captcha qo'shish
    
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'text']
