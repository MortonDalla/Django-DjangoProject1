"""
Definition of forms.
"""
from django.forms import ModelForm
from .models import RegisterUsers

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class RegisterUsersForm(ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "First Name"}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Last Name"}))
    user_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "User Name"}))
    password = forms.PasswordInput()
    description = forms.CharField(widget=forms.Textarea(
        attrs={
            'cols': 100,
            'rows': 12}
    ))
    email_address = forms.EmailField()
    contact_numbers = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = RegisterUsers
        fields = [
            'first_name',
            'last_name',
            'user_name',
            'password',
            'email_address',
            'description',
            'contact_numbers'
        ]

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))

    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))