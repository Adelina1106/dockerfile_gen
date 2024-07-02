from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    email = forms.EmailField(label='Email')
    username = forms.CharField(max_length=30, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.replace(' ', '').isalpha():
            raise ValidationError(_('First name must contain only letters.'))
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.replace(' ', '').isalpha():
            raise ValidationError(_('Last name must contain only letters.'))
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(_('Email address is already registered.'))
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            password_validation.validate_password(password, self.instance)
        except ValidationError as e:
            self.add_error('password', e)
        return password