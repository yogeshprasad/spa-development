from django import forms
from django.core.validators import RegexValidator, validate_slug, validate_email, MinLengthValidator

class CoachingContactForm(forms.Form):
    email = forms.EmailField(validators=[validate_email])
    mobile = forms.IntegerField()
    city = forms.CharField()
    address = forms.CharField()
    message = forms.CharField()
    header = forms.CharField()
