from django import forms
from django.core.validators import RegexValidator, validate_slug

class CoachingRegisterationForm(forms.Form):
    coaching_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Java Soft'}))
    unique_url = forms.CharField(validators=[validate_slug],widget=forms.TextInput(attrs={'placeholder': 'javasoft'}))