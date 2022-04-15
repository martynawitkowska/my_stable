from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from . import models


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'company_name', 'email', 'user_type')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise ValidationError("Passwords don't match!")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class AddressForm(forms.ModelForm):
    class Meta:
        model = models.Address
        fields = ('street', 'house_number', 'apartment_number', 'city', 'country', 'postal_code')


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.TextInput(
        attrs={
            'type': 'text',
            'name': 'username',
            'placeholder': 'Email'
        }
    ))

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ('username', 'password')
