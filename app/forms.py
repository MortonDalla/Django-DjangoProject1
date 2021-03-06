"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
import shop_application.models

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    users_enrolled = shop_application.models.RegisterUsers.objects.all()
    print(users_enrolled)
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))

    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Password'}))

    class Meta:
        model = shop_application.models.RegisterUsers
        fields = [
            'username',
            'password',
            ]


class Register_Users(forms.ModelForm):
    user_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "User Name"}))
    password = forms.PasswordInput()
    email = forms.EmailField()
    description = forms.CharField(widget=forms.Textarea(
        attrs={
            'cols': 100,
            'rows': 12}
    ))
    contact_numbers = forms.NumberInput()

    # def clean_email(self, *args, **kwargs):
    #     email = self.cleaned_data.get("email")
    #     if not email.endswith("com"):
    #         raise forms.ValidationError("This is not a valid email address")
    #     return email
    class Meta:
        model = shop_application.models.RegisterUsers
        fields = [
            'user_name',
            'password',
            'email',
            'description',
            'contact_numbers'
        ]

# class RawProductForm(forms.Form):
# #     user_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "User Name"}))
# #     password = forms.PasswordInput(required=True)
# #     email = forms.EmailField()
# #     description = forms.CharField(widget=forms.Textarea(
# #         attrs={
# #             'cols': 100,
# #             'rows': 12}
# #     ))
# #     contact_numbers = forms.NumberInput()