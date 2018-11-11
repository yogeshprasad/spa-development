from django import forms
from django.core.validators import RegexValidator, validate_slug

class CoachingRegisterationForm(forms.Form):
    coaching_name = forms.CharField()
    unique_url = forms.CharField(validators=[validate_slug])